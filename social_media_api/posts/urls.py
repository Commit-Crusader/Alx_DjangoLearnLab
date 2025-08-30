# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

# Create a router for automatic URL generation
router = DefaultRouter()

# Register ViewSets - this creates all standard REST endpoints
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

# The router automatically creates these URLs:
# 
# POSTS:
# GET    /api/posts/              -> list all posts
# POST   /api/posts/              -> create new post  
# GET    /api/posts/{id}/         -> get specific post
# PUT    /api/posts/{id}/         -> update post (full)
# PATCH  /api/posts/{id}/         -> update post (partial)
# DELETE /api/posts/{id}/         -> delete post
#
# CUSTOM POST ACTIONS:
# GET    /api/posts/{id}/comments/    -> get post's comments
# GET    /api/posts/my_posts/         -> get current user's posts
# POST   /api/posts/{id}/add_comment/ -> add comment to post
#
# COMMENTS:
# GET    /api/comments/           -> list all comments
# POST   /api/comments/           -> create new comment
# GET    /api/comments/{id}/      -> get specific comment  
# PUT    /api/comments/{id}/      -> update comment (full)
# PATCH  /api/comments/{id}/      -> update comment (partial)
# DELETE /api/comments/{id}/      -> delete comment
#
# CUSTOM COMMENT ACTIONS:
# GET    /api/comments/my_comments/   -> get current user's comments
# GET    /api/comments/recent/        -> get recent comments

urlpatterns = [
    path('', include(router.urls)),
]