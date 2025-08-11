from django.shortcuts import render
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


class RegisterView(CreateView):
    """
    User registration view using Django's built-in UserCreationForm
    """
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')



