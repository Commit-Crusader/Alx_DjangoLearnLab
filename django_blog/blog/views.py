from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseRedirect

from .models import Post, Comment
from .forms import CustomUserCreationForm, UserUpdateForm, PostForm, CommentForm


# ---------------------------
# User Authentication & Profile
# ---------------------------

def register(request):
    """User registration with auto-login"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """User profile update"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'registration/profile.html', {
        'form': form,
        'user': request.user
    })


# ---------------------------
# Blog Post Views
# ---------------------------

class PostListView(ListView):
    """List all blog posts (paginated)"""
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']  # Now using the correct field name
    paginate_by = 5


class PostDetailView(DetailView):
    """Display single post with comments"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        # Comments & form
        context['comments'] = Comment.objects.filter(post=post).select_related('author')
        context['comment_count'] = context['comments'].count()
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new blog post"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing post (only by author)"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a blog post (only by author)"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog-home')

    def test_func(self):
        return self.request.user == self.get_object().author


# ---------------------------
# Comment Views
# ---------------------------

@login_required
def add_comment(request, post_id):
    """Function-based view for adding a comment"""
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added successfully!')
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update a comment (only by author)"""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/edit_comment.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a comment (only by author)"""
    model = Comment
    template_name = 'blog/delete_comment.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your comment has been deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})


class CommentListView(ListView):
    """List all comments (with optional filters)"""
    model = Comment
    template_name = 'blog/comment_list.html'
    context_object_name = 'comments'
    paginate_by = 20
    ordering = ['-created_at']


@login_required
@require_POST
def quick_add_comment(request, post_id):
    """AJAX endpoint for quick comment addition"""
    post = get_object_or_404(Post, id=post_id)
    
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        
        return JsonResponse({
            'success': True,
            'comment_id': comment.id,
            'author': comment.author.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime("%B %d, %Y at %I:%M %p")
        })
    
    return JsonResponse({
        'success': False,
        'errors': form.errors
    })


@login_required
def profile(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    context = {
        'user_posts': user_posts
    }
    return render(request, 'registration/profile.html', context)
