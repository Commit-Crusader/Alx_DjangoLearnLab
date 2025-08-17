from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book, Author
from .serializers import BookSerializer
from rest_framework.response import Response

class BookListView(generics.ListAPIView):
    """
    View to list all books
    GET /books/ - Returns list of all books
    GET /books/?author=1 -Books by author with ID 1
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
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