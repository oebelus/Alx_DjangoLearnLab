from .views import NotificationView
from django.urls import path

urlpatterns = [
    path('notifications/', NotificationView.as_view(), name='notifications'),
]