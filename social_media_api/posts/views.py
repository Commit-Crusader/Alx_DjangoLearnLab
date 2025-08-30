# posts/views.py
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .pagination import CustomPageNumberPagination


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission: only authors can edit their own content
    Others can only read
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for the author
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    Complete ViewSet for Posts with all CRUD operations + custom actions
    
    Provides:
    - list: GET /posts/
    - create: POST /posts/
    - retrieve: GET /posts/{id}/
    - update: PUT /posts/{id}/
    - partial_update: PATCH /posts/{id}/
    - destroy: DELETE /posts/{id}/
    - Custom actions (see below)
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination
    
    # Add filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']  # Search by title or content
    filterset_fields = ['author']  # Filter by author
    ordering_fields = ['created_at', 'updated_at', 'title']  # Allow sorting
    ordering = ['-created_at']  # Default: newest first

    def perform_create(self, serializer):
        """
        Set the author when creating a post
        This ensures the logged-in user becomes the author
        """
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Custom action: Get all comments for a specific post
        URL: GET /posts/{id}/comments/
        """
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """
        Custom action: Get current user's posts only
        URL: GET /posts/my_posts/
        """
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        
        posts = self.queryset.filter(author=request.user)
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """
        Custom action: Add a comment to a specific post
        URL: POST /posts/{id}/add_comment/
        """
        post = self.get_object()
        
        # Create comment data with the post and author
        comment_data = request.data.copy()
        comment_data['post'] = post.id
        
        serializer = CommentSerializer(data=comment_data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Complete ViewSet for Comments with all CRUD operations + custom actions
    
    Provides all standard operations:
    - list: GET /comments/
    - create: POST /comments/
    - retrieve: GET /comments/{id}/
    - update: PUT /comments/{id}/
    - partial_update: PATCH /comments/{id}/
    - destroy: DELETE /comments/{id}/
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination
    
    # Filter and order comments
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['post', 'author']  # Filter by post or author
    search_fields = ['content']  # Search comment content
    ordering_fields = ['created_at']  # Allow sorting by date
    ordering = ['created_at']  # Default: oldest first

    def perform_create(self, serializer):
        """
        Set the author when creating a comment
        """
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def my_comments(self, request):
        """
        Custom action: Get current user's comments only
        URL: GET /comments/my_comments/
        """
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        
        comments = self.queryset.filter(author=request.user)
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Custom action: Get recent comments (last 24 hours)
        URL: GET /comments/recent/
        """
        from django.utils import timezone
        from datetime import timedelta
        
        yesterday = timezone.now() - timedelta(days=1)
        recent_comments = self.queryset.filter(created_at__gte=yesterday)
        
        page = self.paginate_queryset(recent_comments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(recent_comments, many=True)
        return Response(serializer.data)