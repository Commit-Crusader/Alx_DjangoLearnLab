# posts/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination with more info and flexible page size
    """
    page_size = 10  # Default items per page
    page_size_query_param = 'page_size'  # Allow ?page_size=20
    max_page_size = 100  # Maximum items per page
    
    def get_paginated_response(self, data):
        """
        Return custom pagination response with extra info
        """
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,  # Total items
            'total_pages': self.page.paginator.num_pages,  # Total pages
            'current_page': self.page.number,  # Current page number
            'page_size': self.get_page_size(self.request),  # Items per page
            'results': data  # The actual data
        })