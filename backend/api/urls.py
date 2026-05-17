from rest_framework import routers
from django.urls import path, include
from .views import UserViewSet, TaskViewSet, OrderViewSet, ReviewViewSet, MessageViewSet, ReportViewSet, BlacklistViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'blacklist', BlacklistViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
