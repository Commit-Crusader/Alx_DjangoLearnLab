from django.db.models import Q
from .models import Post, Category, Tag

class PostSearchEngine:
    """
    Advanced search functionality for blog posts
    """
    
    @staticmethod
    def search_posts(query, filters=None):
        """
        Comprehensive search across all post fields
        
        Args:
            query (str): Search query
            filters (dict): Additional filters like category, tag, date range
            
        Returns:
            QuerySet: Filtered posts
        """
        if not query:
            return Post.objects.all()
        
        # Base search across multiple fields
        search_filters = Q()
        
        # Search in title and content
        search_filters |= Q(title__icontains=query)
        search_filters |= Q(content__icontains=query)
        
        # Search in author username, first name, last name
        search_filters |= Q(author__username__icontains=query)
        search_filters |= Q(author__first_name__icontains=query)
        search_filters |= Q(author__last_name__icontains=query)
        
        # Search in category name
        search_filters |= Q(category__name__icontains=query)
        
        # Search in tags
        search_filters |= Q(tags__name__icontains=query)
        
        posts = Post.objects.filter(search_filters).distinct()
        
        # Apply additional filters
        if filters:
            if filters.get('category'):
                posts = posts.filter(category__slug=filters['category'])
            if filters.get('tag'):
                posts = posts.filter(tags__slug=filters['tag'])
            if filters.get('date_from'):
                posts = posts.filter(published_date__gte=filters['date_from'])
            if filters.get('date_to'):
                posts = posts.filter(published_date__lte=filters['date_to'])
        
        return posts.order_by('-published_date')
    
    @staticmethod
    def get_search_suggestions(query, limit=5):
        """
        Get search suggestions based on query
        
        Args:
            query (str): Search query
            limit (int): Number of suggestions to return
            
        Returns:
            list: Search suggestions
        """
        if not query or len(query) < 2:
            return []
        
        suggestions = []
        
        # Suggestions from post titles
        title_suggestions = Post.objects.filter(
            title__icontains=query
        ).values_list('title', flat=True).distinct()[:limit]
        suggestions.extend(list(title_suggestions))
        
        # Suggestions from categories
        category_suggestions = Category.objects.filter(
            name__icontains=query
        ).values_list('name', flat=True).distinct()[:limit//2]
        suggestions.extend(list(category_suggestions))
        
        # Suggestions from tags
        tag_suggestions = Tag.objects.filter(
            name__icontains=query
        ).values_list('name', flat=True).distinct()[:limit//2]
        suggestions.extend(list(tag_suggestions))
        
        return suggestions[:limit]
    
    @staticmethod
    def get_popular_searches():
        """
        Get popular search terms (could be implemented with analytics)
        
        Returns:
            list: Popular search terms
        """
        # This could be enhanced with actual analytics
        return [
            'django', 'python', 'tutorial', 'web development', 
            'javascript', 'database', 'api'
        ]
