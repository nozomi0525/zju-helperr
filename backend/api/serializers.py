from rest_framework import serializers
from .models import User, Task, Order, Review, Message, Report, Blacklist

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    publish_count = serializers.SerializerMethodField()
    accept_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id','username','password','first_name','last_name','phone','wechat','avatar','credit_score','publish_count','accept_count']

    def get_publish_count(self, obj):
        return obj.published.count()

    def get_accept_count(self, obj):
        return obj.orders.count()

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

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('status', 'publisher', 'created_at', 'updated_at', 'publisher_contact')
        extra_kwargs = {
            'contact_info': {'write_only': True},
        }

    def get_publisher_contact(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None
        is_acceptor = obj.orders.filter(status='pending', acceptor=request.user).exists()
        if is_acceptor:
            return obj.contact_info or None
        return None

    def validate(self, attrs):
        if self.instance is None and not (attrs.get('contact_info') or '').strip():
            raise serializers.ValidationError({'contact_info': '请填写联系方式'})
        if attrs.get('contact_info'):
            attrs['contact_info'] = attrs['contact_info'].strip()
        return attrs

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('status', 'acceptor', 'publisher_confirmed', 'acceptor_confirmed', 'created_at')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

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
