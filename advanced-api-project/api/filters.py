# api/filters.py
import django_filters
from .models import Book, Author

class BookFilter(django_filters.FilterSet):
    """
    Custom filter class for Book model
    Provides various filtering options for the Book API
    """
    
    # Exact match filters
    title = django_filters.CharFilter(lookup_expr='icontains')  # Case-insensitive contains
    author = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    publication_year = django_filters.NumberFilter()
    
    # Range filters
    publication_year__gte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gte')  # Greater than or equal
    publication_year__lte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lte')  # Less than or equal
    
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'publication_year': ['exact', 'gte', 'lte'],
            'author__name': ['exact', 'icontains'],
        }