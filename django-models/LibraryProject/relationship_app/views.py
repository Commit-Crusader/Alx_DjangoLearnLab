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

# Admin-only view
@user_passes_test(is_admin)
def admin_view(request):
    """View accessible only by Admin users"""
    return render(request, 'admin_view.html', {'user_role': 'Admin'})

# Librarian-only view
@user_passes_test(is_librarian)
def librarian_view(request):
    """View accessible only by Librarian users"""
    return render(request, 'librarian_view.html', {'user_role': 'Librarian'})

# Member-only view
@user_passes_test(is_member)
def member_view(request):
    """View accessible only by Member users"""
    return render(request, 'member_view.html', {'user_role': 'Member'})
