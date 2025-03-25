from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from .serializers import PostSerializer, CommentSerializer
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, permissions,status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework.views import APIView
from .models import Post, Comment, Like
from rest_framework import viewsets
from rest_framework import filters

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFiltere]
    filterset_fields = ['title', 'content']
    search_fields = ['title', 'content']

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class FeedView(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)   
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LikeView(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk, *args, **kwargs):
        post = generics.get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            Notification.objects.create(
                recipient = post.author,
                actor = request.user,
                verb = 'liked',
                content_type = ContentType.objects.get_for_model(Post),
                object_id = post.id
            )
            return Response({'message': 'Post liked'}, status=status.HTTP_200_OK)

        else:
            like.delete()
            return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)
     