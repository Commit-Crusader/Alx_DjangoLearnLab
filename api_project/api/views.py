from rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer

# Create your views here.

class BookList(generics.ListAPIView):
    """
    API view to retrieve a list of all books.
    
    This view extends ListAPIView which provides GET method handler
    for listing a queryset of model instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permsission_classes = [permissions.IsAuthenticated]
