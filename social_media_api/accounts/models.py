from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    followers = models.ManyToManyField('self', related_name='user_following', symmetrical=False)
    following = models.ManyToManyField('self', related_name='user_followers', symmetrical=False)

    groups = models.ManyToManyField(
        Group, related_name='customuser_groups', blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name='customuser_permissions', blank=True
    )