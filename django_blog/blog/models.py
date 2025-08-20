from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Rename from published_date
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    
class Comment(models.Model):
    """Model for blog post comments"""
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text="The post this comment belongs to"
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text="The user who wrote this comment"
    )
    content = models.TextField(
        max_length=1000,
        help_text="The content of the comment"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the comment was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the comment was last updated"
    )
    
    class Meta:
        ordering = ['created_at']  # Show oldest comments first
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk}) + f'#comment-{self.pk}'
