from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import F
from .models import User, Task, Order, Review, Message, Report, Blacklist
from .serializers import UserSerializer, TaskSerializer, OrderSerializer, ReviewSerializer, MessageSerializer, ReportSerializer, BlacklistSerializer
from django.db.models import Avg

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
        role = request.data.get('as_role')
        if role == 'publisher':
            order.publisher_confirmed = True
        elif role == 'acceptor':
            order.acceptor_confirmed = True
        order.save()
        if order.publisher_confirmed and order.acceptor_confirmed:
            order.status = 'completed'
            order.task.status = 'completed'
            order.task.save()
            order.save()
        return Response({'status': 'ok'})

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        review = serializer.save()
        # update target credit score
        avg = Review.objects.filter(target=review.target).aggregate(avg=Avg('rating'))['avg']
        review.target.credit_score = avg or review.target.credit_score
        review.target.save()

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
