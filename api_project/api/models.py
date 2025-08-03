from django.db import models
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=200, default="Unknown Book")
    author = models.CharField(max_length=100, default="Unknown Author")
    published_date = models.DateField(default=timezone.now)  # Use current date as default
    
    
    def __str__(self):
        return self.title
