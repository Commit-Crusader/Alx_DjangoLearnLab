from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy, reverse
from .forms import UserRegisterForm, PostForm, CommentForm
from .models import Post, Comment, Category, Tag

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

class PostListView(ListView):
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
        category_slug = self.request.GET.get('category')
        tag_slug = self.request.GET.get('tag')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['current_category'] = self.request.GET.get('category', '')
        context['current_tag'] = self.request.GET.get('tag', '')
        return context

class PostDetailView(DetailView):
    """
    Display a single blog post
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
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
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        messages.error(self.request, 'You can only edit your own posts!')
        return redirect('post_detail', pk=self.get_object().pk)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a blog post (author only)
    """
    model = Post
    template_name = 'blog/post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        messages.error(self.request, 'You can only delete your own posts!')
        return redirect('post_detail', pk=self.get_object().pk)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Category and Tag views
class CategoryListView(ListView):
    """
    Display all categories
    """
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10

class CategoryDetailView(DetailView):
    """
    Display posts for a specific category
    """
    model = Category
    template_name = 'blog/category_detail.html'
    context_object_name = 'category'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['posts'] = Post.objects.filter(category=category).order_by('-published_date')
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class TagListView(ListView):
    """
    Display all tags
    """
    model = Tag
    template_name = 'blog/tag_list.html'
    context_object_name = 'tags'
    paginate_by = 10

class TagDetailView(DetailView):
    """
    Display posts for a specific tag
    """
    model = Tag
    template_name = 'blog/tag_detail.html'
    context_object_name = 'tag'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.get_object()
        context['posts'] = Post.objects.filter(tags=tag).order_by('-published_date')
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

# Comment functionality 
#class CommentCreateView(LoginRequiredMixin, CreateView):
# Comment Views
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added successfully!')
            return redirect('post_detail', pk=post.pk)
        else:
            messages.error(request, 'There was an error with your comment. Please try again.')
    
    return redirect('post_detail', pk=post.pk)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_update.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        messages.success(self.request, 'Your comment has been updated successfully!')
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})
    
    def handle_no_permission(self):
        messages.error(self.request, 'You can only edit your own comments.')
        return redirect('post_detail', pk=self.get_object().post.pk)

""""class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_delete.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        messages.success(self.request, 'Your comment has been deleted successfully!')
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})
    
    def handle_no_permission(self):
        messages.error(self.request, 'You can only delete your own comments.')
        return redirect('post_detail', pk=self.get_object().post.pk)
"""
# Alternative function-based view for comment deletion
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    post_pk = comment.post.pk
    
    if request.user != comment.author:
        messages.error(request, 'You can only delete your own comments.')
        return redirect('post_detail', pk=post_pk)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Your comment has been deleted successfully!')
    
    return redirect('post_detail', pk=post_pk)
