from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length = 100)
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length = 200)
    book = models.ManyToManyField(Book)


    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length = 100)
    library = models.OneToOneField(Library, on_delete = models.CASCADE)


    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = [
            ('Admin', 'Admin'),
            ('Librarian', 'Librarian'),
            ('Member', 'Member'),
        ]

    user = models.OneToOneField(
            User, 
            on_delete = models.CASCADE, 
            help_text="Link to Django's built-in User Model"
        )

    role = models.CharField(
            max_length=20,
            choices=ROLE_CHOICES,
            default='Member',
            help_text="User's role in the system"
            )

    def __str(self):
        return f"{self.user.username} - {self.role}"


    # Django Signals for automatic UserProfile creation
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver that creates a UserProfile whenever a new User is created
    """
    if created:
        UserProfile.objects.create(user=instance)
        print(f"UserProfile created for user: {instance.username}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal receiver that saves the UserProfile whenever the User is saved
    """
    # Check if the user has a profile, create one if it doesn't exist
    if not hasattr(instance, 'userprofile'):
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()
