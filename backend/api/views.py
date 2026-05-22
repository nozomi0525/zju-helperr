from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import F
from .models import User, Task, Order, Review, Message, Report, Blacklist
from .serializers import UserSerializer, TaskSerializer, OrderSerializer, ReviewSerializer, MessageSerializer, ReportSerializer, BlacklistSerializer
from .credit import recalculate_credit_score

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        return User.objects.all()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_reviews(self, request):
        reviews = (
            Review.objects.filter(target=request.user)
            .select_related('reviewer', 'order', 'order__task')
            .order_by('-created_at')[:20]
        )
        data = [
            {
                'rating': r.rating,
                'comment': r.comment,
                'reviewer_username': r.reviewer.username,
                'task_title': r.order.task.title,
                'created_at': r.created_at,
            }
            for r in reviews
        ]
        return Response(data)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def reviews(self, request, pk=None):
        user = self.get_object()
        reviews = (
            Review.objects.filter(target=user)
            .select_related('reviewer', 'order', 'order__task')
            .order_by('-created_at')[:20]
        )
        data = [
            {
                'rating': r.rating,
                'comment': r.comment,
                'reviewer_username': r.reviewer.username,
                'task_title': r.order.task.title,
                'created_at': r.created_at,
            }
            for r in reviews
        ]
        return Response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.perform_create(serializer)
        except IntegrityError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(publisher=user)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                self.perform_create(serializer)
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError({'detail': str(e)})
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = self.request.user
        task = serializer.validated_data.get('task')
        if task.publisher_id == user.id:
            raise ValidationError('不能接自己发布的任务')
        if task.status != 'active':
            raise ValidationError('该任务当前不可接单')
        if task.orders.filter(status='pending').exists():
            raise ValidationError('该任务已被接单')
        serializer.save(acceptor=user)
        task.status = 'accepted'
        task.save(update_fields=['status', 'updated_at'])
        User.objects.filter(pk=user.pk).update(accept_count=F('accept_count') + 1)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()
        user = request.user
        if order.status != 'pending':
            raise ValidationError('该订单已结束，无法再次确认')
        if order.task.publisher_id == user.id:
            if order.publisher_confirmed:
                raise ValidationError('您已确认过完成')
            order.publisher_confirmed = True
        elif order.acceptor_id == user.id:
            if order.acceptor_confirmed:
                raise ValidationError('您已确认过完成')
            order.acceptor_confirmed = True
        else:
            raise ValidationError('无权操作该订单')
        order.save(update_fields=['publisher_confirmed', 'acceptor_confirmed'])
        if order.publisher_confirmed and order.acceptor_confirmed:
            order.status = 'completed'
            order.task.status = 'completed'
            order.task.save(update_fields=['status', 'updated_at'])
            order.save(update_fields=['status'])
        serializer = self.get_serializer(order)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                self.perform_create(serializer)
        except ValidationError:
            raise
        except IntegrityError:
            raise ValidationError({'detail': '您已评价过该订单'})
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = self.request.user
        order = serializer.validated_data['order']
        if order.status != 'completed':
            raise ValidationError('订单完成后才能评价')
        if order.reviews.filter(reviewer=user).exists():
            raise ValidationError('您已评价过该订单')

        task = order.task
        if task.publisher_id == user.id:
            target = order.acceptor
            role_type = 'publisher'
        elif order.acceptor_id == user.id:
            target = task.publisher
            role_type = 'acceptor'
        else:
            raise ValidationError('无权评价该订单')

        review = serializer.save(reviewer=user, target=target, role_type=role_type)
        recalculate_credit_score(target)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer
    permission_classes = [AllowAny]

class BlacklistViewSet(viewsets.ModelViewSet):
    queryset = Blacklist.objects.all().order_by('-created_at')
    serializer_class = BlacklistSerializer
    permission_classes = [AllowAny]
