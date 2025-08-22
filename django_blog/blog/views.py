from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest
from .forms import UserRegisterForm, PostForm
from .models import Post

def home_view(request):
    """
    Display the home page with recent blog posts
    """
    recent_posts = Post.objects.all().order_by('-published_date')[:5]
    context = {
        'recent_posts': recent_posts
    }
    return render(request, 'blog/home.html', context)

def register_view(request):
    """
    Handle user registration
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save()
            # Log the user in automatically after registration
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')  # Redirect to profile page
    else:
        form = UserRegisterForm()
    
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile_view(request):
    """
    Display user profile page - requires login
    """
    user_posts = Post.objects.filter(author=request.user).order_by('-published_date')
    context = {
        'user': request.user,
        'user_posts': user_posts
    }
    return render(request, 'blog/profile.html', context)

@login_required
def edit_profile_view(request):
    """
    Allow users to edit their profile information
    """
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        
        # Update user information
        user = request.user
        user.email = email
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'blog/edit_profile.html', {'user': request.user})

def post_list_view(request):
    """
    Display all blog posts with pagination and search
    """
    # Get all posts ordered by newest first
    posts = Post.objects.all().order_by('-published_date')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query
    }
    return render(request, 'blog/post_list.html', context)

def post_detail_view(request, post_id):
    """
    Display a single blog post
    """
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def create_post_view(request):
    """
    Create a new blog post
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'title': 'Create New Post'
    }
    return render(request, 'blog/create_post.html', context)

@login_required
def edit_post_view(request, post_id):
    """
    Edit an existing blog post (author only)
    """
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the user is the author
    if post.author != request.user:
        messages.error(request, 'You can only edit your own posts!')
        return redirect('post_detail', post_id=post.id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated successfully!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
        'title': 'Edit Post'
    }
    return render(request, 'blog/edit_post.html', context)

@login_required
def delete_post_view(request, post_id):
    """
    Delete a blog post (author only)
    """
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the user is the author
    if post.author != request.user:
        messages.error(request, 'You can only delete your own posts!')
        return redirect('post_detail', post_id=post.id)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted successfully!')
        return redirect('post_list')
    
    context = {
        'post': post
    }
    return render(request, 'blog/delete_post.html', context)
