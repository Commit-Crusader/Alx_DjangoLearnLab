from django.shortcuts import render, redirect
from .models import Library, Author, Librarian, Book
from django.views.generic import DetailView
from django.views.generic.detail import DetailView
from django.contrib.auth import login as login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.


def list_books(request):
    books = Book.objects.all()
    context = {'book_list': books}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    """A class-based view for displaying details of a specific library."""
    model = Library
    template_name = 'relationship_app/library_detail.html'


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('list_books')  # Redirect to your main page
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def is_admin(user):
    #Check if user has Admin Role
    #but first we need to check if the user is even logged in

    if not user.is_authenticated:
        return False
    try:
        return user.profile.role == 'Admin'
    except:
        return False

def is_librarian(user):
    if not user.is_authenticated:
        return False
    try:
        return user.profile.role == 'Librarian'
    except:
        return False

def is_member(user):
    if not user.is_authenticated:
        return False
    try:
        return user.profile.role == 'Member'
    except:
        return False

@login_required  # User must be logged in
@user_passes_test(is_admin)  # User must pass the is_admin test
def admin_view(request):
    """
    Admin-only view - accessible only to users with Admin role
    """
    context = {
        'user': request.user,
        'role': request.user.userprofile.role,
        'page_title': 'Admin Dashboard',
        'message': 'Welcome to the Admin Dashboard. You have full system access.'
    }
    return render(request, 'admin_view.html', context)

@login_required  # User must be logged in
@user_passes_test(is_librarian)  # User must pass the is_librarian test
def librarian_view(request):
    """
    Librarian-only view - accessible only to users with Librarian role
    """
    context = {
        'user': request.user,
        'role': request.user.userprofile.role,
        'page_title': 'Librarian Dashboard',
        'message': 'Welcome to the Librarian Dashboard. You can manage books and members.'
    }
    return render(request, 'librarian_view.html', context)

@login_required  # User must be logged in  
@user_passes_test(is_member)  # User must pass the is_member test
def member_view(request):
    """
    Member-only view - accessible only to users with Member role
    """
    context = {
        'user': request.user,
        'role': request.user.userprofile.role,
        'page_title': 'Member Dashboard', 
        'message': 'Welcome to the Member Dashboard. You can browse and borrow books.'
    }
    return render(request, 'member_view.html', context)
