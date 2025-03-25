from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Comment

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = '__all__'

    def validate(self, data):
        if "forbidden_content" in data.get('content', ''):
            raise ValidationError("No forbidden words allowed")

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    
    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, data):
        if "forbidden_content" in data.get('content', ''):
            raise ValidationError("No forbidden words allowed")