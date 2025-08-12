
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import Author, Book, Librarian, Library, UserProfile
from django.template import loader
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth import login as auth_login
# Create your views here.

# Role checking functions
def is_admin(user):
    """Check if user has Admin role"""
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.role =='Admin'
    except UserProfile.DoesNotExist:
        return False

def is_librarian(user):
    """Check if user has Librarian role"""
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.role =='Librarian'
    except UserProfile.DoesNotExist:
        return False

def is_member(user):
    """Check if user has Member role"""
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.role =='Member'
    except UserProfile.DoesNotExist:
        return False

# Role-based views
@user_passes_test(is_member)
def member_view(request):
    """View accessible only by Member users"""
    return render(request, 'relationship_app/member_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    """View accessible only by Librarian users"""
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_admin)
def admin_view(request):
    """View accessible only by Admin users"""
    return render(request, 'relationship_app/admin_view.html')

# Other views
def index(request):
    """Home page view"""
    return HttpResponse('Hello and welcome?')

def list_books(request):
    """Display list of all books"""
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)

# Class-based views
class LibraryDetailView(DetailView):
    """Detail view for Library with associated books"""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        context['books'] = library.books.all()
        return context

class register(CreateView):
    """User registration view"""
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'relationship_app/register.html'

class ProfileView(TemplateView):
    """User profile view"""
    template_name = 'relationship_app/profile.html'

# View to add a new book - requires 'can_add_book' permission
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """View to add a new book"""
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')

        if title and author_id:
            author = get_object_or_404(Author, id=author_id)
            Book.objects.create(title=title, author=author)
            return redirect('list_books')

    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})

# View to edit an existing book - requires 'can_change_book' permission
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    """View to edit an existing book"""
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')

        if title and author_id:
            author = get_object_or_404(Author, id=author_id)
            book.title = title
            book.author = author
            book.save()
            return redirect('list_books')

    authors = Author.objects.all()
    context = {'book': book, 'authors': authors}
    return render(request, 'relationship_app/edit_book.html', context)

# View to delete a book - requires 'can_delete_book' permission
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """View to delete a book"""
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.delete()
        return redirect('list_books')

    return render(request, 'relationship_app/delete_book.html', {'book': book})
