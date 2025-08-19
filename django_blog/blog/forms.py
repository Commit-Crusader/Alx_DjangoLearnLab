from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from .models import Comment
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 10
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom styling to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
class CommentForm(forms.ModelForm):
    """Form for creating and updating comments"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your thoughts...',
                'required': True,
            })
        }
        labels = {
            'content': 'Your Comment'
        }
        help_texts = {
            'content': 'Maximum 1000 characters. Be respectful and constructive.'
        }
    
    def clean_content(self):
        """Custom validation for comment content"""
        content = self.cleaned_data.get('content')
        
        if not content or not content.strip():
            raise ValidationError("Comment cannot be empty.")
        
        if len(content.strip()) < 5:
            raise ValidationError("Comment must be at least 5 characters long.")
        
        # Check for inappropriate content (basic example)
        inappropriate_words = ['spam', 'hate', 'abuse']  # Extend as needed
        content_lower = content.lower()
        for word in inappropriate_words:
            if word in content_lower:
                raise ValidationError(f"Please avoid using inappropriate language.")
        
        return content.strip()
    
    def save(self, commit=True):
        """Override save to handle additional processing if needed"""
        comment = super().save(commit=False)
        
        if commit:
            comment.save()
        
        return comment