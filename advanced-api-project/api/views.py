from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from .models import Book, Author
from .serializers import BookSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import BookFilter
from django_filters import rest_framework

class BookListView(generics.ListAPIView):
    """
    Enhanced Book List API with filtering, searching, and ordering
    
    Features:
    - Filter by title, author, publication_year
    - Search across title and author fields
    - Order by any field (default: title)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow any user to access this view
    
    # Filter backend for advanced filtering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filterset class for Book model
    filterset_class = BookFilter
    
    # Search fields for searching across title and author
    search_fields = ['title', 'author__name']
    
    # Ordering fields for ordering results
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering by title
    
    def get_queryset(self):
        """
        Custom method to filter books by author if requested
        """
        queryset = Book.objects.all()
        author_id = self.request.query_params.get('author', None)
        if author_id is not None:
            queryset = queryset.filter(author_id=author_id)
        return queryset

    
class BookDetailView(generics.RetrieveAPIView):
    """
    View to get a single book by ID
    GET /books/1/ - Returns book with ID 1
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookCreateView(generics.CreateAPIView):
    """
    View to create a new book
    POST /books/create/ - Creates a new book
    Requires authentication
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        """
        Custom method called when creating a book
        """
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    """
    View to update an existing book
    PUT /books/1/update/ - Updates book with ID 1
    Requires authentication
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_update(self, serializer):
        serializer.save

class BookDeleteView(generics.DestroyAPIView):
    """
    View to delete a book
    DELETE /books/1/delete/ - Deletes book with ID 1
    Requires authentication
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_delete(self, instance):
        instance.delete()