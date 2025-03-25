from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            bio=validated_data['bio'],
            profile_picture=validated_data['profile_picture'], 
            **validated_data
        )

        Token.objects.create(user=user)
        
        return user
    
class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = get_user_model().objects.filter(username=data['username']).first()
        if user is None:
            raise serializers.ValidationError('CustomUser does not exist')
        if not user.check_password(data['password']):
            raise serializers.ValidationError('Incorrect password')
        return user