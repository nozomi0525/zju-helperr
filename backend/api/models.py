from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    phone = models.CharField(max_length=32, blank=True, null=True)
    wechat = models.CharField(max_length=64, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    credit_score = models.FloatField(default=5.0)
    publish_count = models.IntegerField(default=0)
    accept_count = models.IntegerField(default=0)

class Task(models.Model):
    CATEGORY_CHOICES = [
        ('agency','agency'),('errand','errand'),('emergency','emergency'),('carpool','carpool'),('other','other')
    ]
    STATUS_CHOICES = [
        ('active', 'active'),
        ('accepted', 'accepted'),
        ('completed', 'completed'),
        ('expired', 'expired'),
    ]
    publisher = models.ForeignKey('User', on_delete=models.CASCADE, related_name='published')
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    is_paid = models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    template_data = models.JSONField(default=dict)
    location = models.CharField(max_length=200, blank=True, null=True)
    deadline = models.CharField(max_length=100, blank=True, null=True)
    reward = models.CharField(max_length=100, blank=True, default='')
    remark = models.TextField(blank=True)
    contact_info = models.CharField(max_length=200, blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    STATUS_CHOICES = [('pending','pending'),('completed','completed'),('cancelled','cancelled')]
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='orders')
    acceptor = models.ForeignKey('User', on_delete=models.CASCADE, related_name='orders')
    publisher_confirmed = models.BooleanField(default=False)
    acceptor_confirmed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

class Review(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='given_reviews')
    target = models.ForeignKey('User', on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    role_type = models.CharField(max_length=32)
    created_at = models.DateTimeField(default=timezone.now)

class Message(models.Model):
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sent_messages')
    to_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='recv_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

class Report(models.Model):
    reporter = models.ForeignKey('User', on_delete=models.CASCADE, related_name='reports')
    target_user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_against')
    target_task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=32, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

class Blacklist(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='blacklists')
    blocked_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='blocked_by')
    created_at = models.DateTimeField(default=timezone.now)
