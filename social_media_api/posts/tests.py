from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post, Comment

User = get_user_model()

class PostCommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.post = Post.objects.create(author=self.user, title='Test Post', content='Content')
    
    def test_create_post(self):
        response = self.client.post('/posts/', {'title': 'New Post', 'content': 'New content'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_posts(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)
    
    def test_create_comment(self):
        response = self.client.post('/comments/', {'post': self.post.id, 'content': 'Nice post!'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_permissions(self):
        other_user = User.objects.create_user(username='other', password='password')
        comment = Comment.objects.create(post=self.post, author=other_user, content='Other comment')
        response = self.client.delete(f'/comments/{comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)