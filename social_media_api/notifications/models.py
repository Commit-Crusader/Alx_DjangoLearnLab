from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications_sent")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications_received")
    verb = models.CharField(max_length=255)  # action text: "liked", "commented", "followed"
    
    # Generic relation (can point to Post, Comment, etc.)
    target_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True, related_name="notifications_targets")
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_ct', 'target_id')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # allow marking as read

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.actor} {self.verb} {self.target} for {self.recipient}"
