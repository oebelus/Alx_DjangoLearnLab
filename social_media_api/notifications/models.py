from django.db import models

class Notification(models.Model):
    recipient = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    actor = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='actor')
    verb = models.CharField(max_length=255)
    target = models.GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)