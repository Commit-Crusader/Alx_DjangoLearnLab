from django.urls import path
from . import views

urlpatterns = [
    # List all books (GET)
    path('books/', views.BookListView.as_view(), name='book-list'),
    
    # Get single book (GET)
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Create new book (POST)
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    
    # Update existing book (PUT/PATCH)
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    
    # Delete book (DELETE)
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
]