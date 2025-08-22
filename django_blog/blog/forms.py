from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

class UserRegisterForm(UserCreationForm):
    """Custom user registration form with email field"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to form fields for styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
    
    def save(self, commit=True):
        """Save the user with email"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts"""
    
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your blog post content here...',
                'rows': 10
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add labels
        self.fields['title'].label = 'Post Title'
        self.fields['content'].label = 'Content'
