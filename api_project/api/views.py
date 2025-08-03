from rest_framework import generics
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
