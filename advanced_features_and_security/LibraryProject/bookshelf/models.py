from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUserManager(BaseUserManager):
    """Custom user manager for handling user creation with additional fields."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """Custom user model extending AbstractUser with additional fields."""
    
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    date_of_birth = models.DateField(
        null=True, 
        blank=True,
    )
    profile_photo = models.ImageField(
        upload_to='profile_photos/', 
        null=True, 
        blank=True,
    )
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username

class Profile(models.Model):
    """User profile model with additional user information."""
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(
        max_length=500, 
        blank=True,
        help_text=_("User's bio/description")
    )
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class Book(models.Model):
    """Book model with security and validation."""
    title = models.CharField(
        max_length=200,
        help_text=_("Book title")
    )
    author = models.CharField(
        max_length=100,
        help_text=_("Book author")
    )
    publication_year = models.IntegerField(
        validators=[
            MinValueValidator(1000, _('Year must be at least 1000')),
            MaxValueValidator(9999, _('Year cannot be more than 9999'))
        ],
        help_text=_("Year of publication")
    )
    isbn = models.CharField(
        max_length=13, 
        unique=True,
        help_text=_("13-digit ISBN")
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='books_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    def __str__(self):
        return self.title

    def clean(self):
        """Validate ISBN format"""
        if not self.isbn.isdigit() or len(self.isbn) != 13:
            raise ValidationError({'isbn': _('ISBN must be exactly 13 digits')})

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile instance when a new CustomUser is created."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """Ensure profile is saved when user is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()