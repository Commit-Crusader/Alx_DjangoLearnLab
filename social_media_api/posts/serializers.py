# posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()  # Gets your custom user model


class AuthorSerializer(serializers.ModelSerializer):
    """Simple serializer for author info"""
    class Meta:
        model = User
        fields = ['id', 'username']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments"""
    author = AuthorSerializer(read_only=True)  # Show author info but don't allow editing
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        """Set the author to current user when creating"""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts"""
    author = AuthorSerializer(read_only=True)  # Show author info
    comments = CommentSerializer(many=True, read_only=True)  # Include all comments
    comments_count = serializers.SerializerMethodField()  # Count of comments
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 
                 'comments', 'comments_count']
        read_only_fields = ['created_at', 'updated_at']

    def get_comments_count(self, obj):
        """Calculate number of comments on this post"""
        return obj.comments.count()

    def create(self, validated_data):
        """Set the author to current user when creating"""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)