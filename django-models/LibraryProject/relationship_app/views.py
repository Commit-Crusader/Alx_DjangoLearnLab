from django.shortcuts import render, redirect
from .models import Library, Author, Librarian, Book
from django.views.generic import DetailView
from django.views.generic.detail import DetailView
from django.contrib.auth import login as login
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
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('list_books')  # Redirect to your main page
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


