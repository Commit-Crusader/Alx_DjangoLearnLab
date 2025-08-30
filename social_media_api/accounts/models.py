from django.db import models
from django.contrib.auth.models import AbstractUser

def profile_upload(instance, filename):
    return f"profile_pictures/{instance.id}/{filename}"

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to=profile_upload, blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followed_by', blank=True)

    @property
    def followers(self):
        return self.followed_by.all()

    @property
    def followers_count(self):
        return self.followed_by.count()

    @property
    def following_count(self):
        return self.following.count()