from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
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

class ListView(ListView):
    """
    Display all blog posts with pagination and search
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-published_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class DetailView( DetailView):
    """
    Display a single blog post
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class CreateView(LoginRequiredMixin, CreateView):
    """
    Create a new blog post
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Post'
        return context

class UpdateView(LoginRequiredMixin, UpdateView):
    """
    Edit an existing blog post (author only)
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'
    context_object_name = 'post'

    def form_valid(self, form):
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Post'
        return context

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            messages.error(request, 'You can only edit your own posts!')
            return redirect('post_detail', pk=post.pk)
        return super().dispatch(request, *args, **kwargs)

class DeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a blog post (author only)
    """
    model = Post
    template_name = 'blog/post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            messages.error(request, 'You can only delete your own posts!')
            return redirect('post_detail', pk=post.pk)
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
