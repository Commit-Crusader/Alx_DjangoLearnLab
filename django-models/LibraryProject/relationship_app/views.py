from django.shortcuts import render, redirect
from .models import Library, Author, Librarian, Book, UserProfile
from django.views.generic import DetailView
from django.views.generic.detail import DetailView
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
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
    """
    Function-based registration view using Django's UserCreationForm
    """
    if request.user.is_authenticated:
            return redirect('login')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        # Create empty form for GET request
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})


