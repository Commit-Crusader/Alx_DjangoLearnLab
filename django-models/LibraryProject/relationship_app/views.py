
from django.shortcuts import render, redirect, HttpResponse
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
def has_role(user, role):
    """Check if user has specific role - optimized version"""
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.role == role
    except UserProfile.DoesNotExist:
        return False

def member_test(user):
    """Test if user has Member role"""
    return has_role(user, 'Member')

def librarian_test(user):
    """Test if user has Librarian role"""
    return has_role(user, 'Librarian')

def admin_test(user):
    """Test if user has Admin role"""
    return has_role(user, 'Admin')

# Role-based views
@user_passes_test(member_test)
def member_view(request):
    """View accessible only by Member users"""
    return render(request, 'relationship_app/member_view.html')

@user_passes_test(librarian_test)
def librarian_view(request):
    """View accessible only by Librarian users"""
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(admin_test)
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
    
