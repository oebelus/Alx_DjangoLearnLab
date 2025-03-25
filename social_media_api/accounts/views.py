from rest_framework.validators import ValidationError
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework import status
from .models import CustomUser

User = get_user_model()

class RegisterUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            raise ValidationError('Please provide all required fields')
        
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Username already exists', status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Email already exists', status.HTTP_400_BAD_REQUEST)
        
        user = CustomUser.objects.create(username=username, email=email, password=password)

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    
class LoginUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            raise ValidationError('Please provide all required fields')

        user = CustomUser.objects.filter(username=username, password=password).first()

        if not user:
            raise ValidationError('Invalid credentials', status.HTTP_400_BAD_REQUEST)

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    
class UserProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'username': user.username,
            'email': user.email,
            'bio': user.bio,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
            'followers': user.followers.count(),
        }

        return Response(data)
    
    def put(self, request):
        user = request.user
        user.profile_picture = request.data.get('profile_picture')
        user.bio = request.data.get('bio')
        user.save()

        return Response({'message': 'Profile updated successfully'})
    
class FollowUserView(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser.objects.all(), id=user_id)
        request.user.following.add(user_to_follow)

        return Response({'message': f'You are now following {user_to_follow.username}'}, status=status.HTTP_200_OK)
    
    def destroy(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser.objects.all(), id=user_id)
        request.user.following.remove(user_to_unfollow)

        return Response({'message': f'You have unfollowed {user_to_unfollow.username}'}, status=status.HTTP_200_OK)