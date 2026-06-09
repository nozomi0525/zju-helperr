from rest_framework import serializers
from .models import User, Task, Order, Review, Message, Report, Blacklist
from .credit import credit_level_label

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    publish_count = serializers.SerializerMethodField()
    accept_count = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    credit_level = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name',
            'phone', 'wechat', 'avatar', 'credit_score', 'credit_level',
            'publish_count', 'accept_count', 'review_count',
        ]

    def get_publish_count(self, obj):
        return obj.published.count()

    def get_accept_count(self, obj):
        # 从订单表统计，不使用 User.accept_count 缓存字段
        return obj.orders.exclude(status='cancelled').count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['publish_count'] = self.get_publish_count(instance)
        data['accept_count'] = self.get_accept_count(instance)
        data['review_count'] = self.get_review_count(instance)
        data['credit_level'] = self.get_credit_level(instance)
        return data

    def get_review_count(self, obj):
        return obj.received_reviews.count()

    def get_credit_level(self, obj):
        return credit_level_label(obj.credit_score)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

class TaskSerializer(serializers.ModelSerializer):
    publisher = UserSerializer(read_only=True)
    publisher_contact = serializers.SerializerMethodField()
    order_info = serializers.SerializerMethodField()
    is_my_accepted = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = (
            'status', 'publisher', 'created_at', 'updated_at',
            'publisher_contact', 'order_info', 'is_my_accepted',
        )
        extra_kwargs = {
            'contact_info': {'write_only': True},
        }

    def get_is_my_accepted(self, obj):
        if hasattr(obj, 'is_my_accepted'):
            return bool(obj.is_my_accepted)
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        # 仅「已接单未完成」置顶，双方确认完成后不再置顶
        return obj.orders.filter(
            acceptor=request.user,
            status='pending',
        ).exists()

    def get_publisher_contact(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None
        order = (
            obj.orders.filter(status__in=['pending', 'completed'])
            .order_by('-created_at')
            .first()
        )
        if not order or order.acceptor_id != request.user.id:
            return None
        contact = (obj.contact_info or '').strip()
        return contact or None

    def get_order_info(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None
        order = (
            obj.orders.filter(status__in=['pending', 'completed'])
            .select_related('acceptor')
            .order_by('-created_at')
            .first()
        )
        if not order:
            return None
        user = request.user
        is_publisher = obj.publisher_id == user.id
        is_acceptor = order.acceptor_id == user.id
        if not (is_publisher or is_acceptor):
            return None

        my_review = order.reviews.filter(reviewer=user).first()
        other_user = order.acceptor if is_publisher else obj.publisher
        contact = (obj.contact_info or '').strip() or None

        return {
            'order_id': order.id,
            'status': order.status,
            'publisher_confirmed': order.publisher_confirmed,
            'acceptor_confirmed': order.acceptor_confirmed,
            'acceptor_username': order.acceptor.username,
            'my_role': 'publisher' if is_publisher else 'acceptor',
            'publisher_contact': contact if is_acceptor else None,
            'can_confirm': order.status == 'pending' and (
                (is_publisher and not order.publisher_confirmed)
                or (is_acceptor and not order.acceptor_confirmed)
            ),
            'can_review': order.status == 'completed' and my_review is None,
            'can_revoke': (
                is_publisher
                and obj.status == 'accepted'
                and order.status == 'pending'
                and not order.publisher_confirmed
                and not order.acceptor_confirmed
            ),
            'can_cancel_accept': (
                is_acceptor
                and obj.status == 'accepted'
                and order.status == 'pending'
                and not order.publisher_confirmed
                and not order.acceptor_confirmed
            ),
            'my_review': {
                'rating': my_review.rating,
                'comment': my_review.comment,
            } if my_review else None,
            'review_target_username': other_user.username,
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user.is_authenticated and instance.publisher_id == request.user.id:
            data['contact_info'] = instance.contact_info or ''
        return data

    def validate(self, attrs):
        if self.instance is None and not (attrs.get('contact_info') or '').strip():
            raise serializers.ValidationError({'contact_info': '请填写联系方式'})
        if 'contact_info' in attrs:
            attrs['contact_info'] = (attrs['contact_info'] or '').strip()
            if not attrs['contact_info']:
                raise serializers.ValidationError({'contact_info': '请填写联系方式'})
        return attrs

class OrderSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = (
            'status', 'acceptor', 'publisher_confirmed',
            'acceptor_confirmed', 'created_at', 'task_title',
        )

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.CharField(source='reviewer.username', read_only=True)
    target_username = serializers.CharField(source='target.username', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'order', 'reviewer', 'target', 'rating', 'comment',
            'role_type', 'created_at', 'reviewer_username', 'target_username',
        ]
        read_only_fields = ('reviewer', 'target', 'role_type', 'created_at', 'reviewer_username', 'target_username')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class BlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blacklist
        fields = '__all__'
