from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view, name='register'),
    path('login/', views.LoginUserView.as_view, name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', views.UserProfileView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', views.UserProfileView.as_view(), name='unfollow'),
]