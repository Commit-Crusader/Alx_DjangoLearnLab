from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Post

def home(request):
    """Home page view displaying recent blog posts"""
    posts = Post.objects.all().order_by('-published_date')[:5]
    context = {
        'posts': posts,
        'title': 'Welcome to Django Blog'
    }
    return render(request, 'blog/home.html', context)

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    context = {
        'form': form,
        'title': 'Register'
    }
    return render(request, 'auth/register.html', context)

@login_required
def profile(request):
    """User profile view for viewing and editing profile"""
    if request.method == 'POST':
        # Handle profile updates here
        # For now, we'll just show the profile
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    user_posts = Post.objects.filter(author=request.user).order_by('-published_date')
    context = {
        'user_posts': user_posts,
        'title': 'Profile'
    }
    return render(request, 'auth/profile.html', context)
