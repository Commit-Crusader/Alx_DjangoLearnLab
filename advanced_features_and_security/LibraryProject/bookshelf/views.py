from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from .models import Book
from .forms import BookForm, BookSearchForm, ExampleForm


# Permission-based views
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """Display list of books with permission check."""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
@csrf_protect
def book_create(request):
    """Create new book with permission check."""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            #messages.success(request, 'Book created successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {'form': form})


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
@csrf_protect
def book_edit(request, pk):
    """Edit existing book with permission check."""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form, 
        'book': book
    })


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """Delete book with permission check."""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

@login_required
def book_search(request):
    """Secure search implementation"""
    query = request.GET.get('q', '')
    
    # Use QuerySet methods instead of raw SQL
    books = Book.objects.filter(title__icontains=query) if query else Book.objects.none()
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'query': escape(query)  # Escape user input for display
    })
    
    
@csrf_protect
def example_form_view(request):
    """Handle the example form with security measures"""
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the cleaned data
            cleaned_data = form.cleaned_data
            messages.success(request, 'Form submitted successfully!')
            return redirect('book_list')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})