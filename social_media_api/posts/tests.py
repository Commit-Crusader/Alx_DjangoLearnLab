from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post, Comment, Like, Notification

User = get_user_model()

class PostCommentLikeNotificationTests(APITestCase):
    def setUp(self):
        # Author of the post
        self.author = User.objects.create_user(username='author', password='password')
        # Another user who will like/unlike and comment
        self.fan = User.objects.create_user(username='fan', password='password')

        # Author creates a post
        self.post = Post.objects.create(author=self.author, title='Test Post', content='Content')

        # Log in as fan (the test client runs as this user)
        self.client.login(username='fan', password='password')

    # -------------------
    # Post tests
    # -------------------
    def test_create_post(self):
        response = self.client.post('/posts/', {'title': 'New Post', 'content': 'New content'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_posts(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)

    # -------------------
    # Comment tests
    # -------------------
    def test_create_comment(self):
        response = self.client.post('/comments/', {'post': self.post.id, 'content': 'Nice post!'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_permissions(self):
        other_user = User.objects.create_user(username='other', password='password')
        comment = Comment.objects.create(post=self.post, author=other_user, content='Other comment')
        response = self.client.delete(f'/comments/{comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -------------------
    # Like tests
    # -------------------
    def test_like_post(self):
        url = f'/posts/{self.post.id}/like/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(user=self.fan, post=self.post).exists())

    def test_unlike_post(self):
        # First like the post
        Like.objects.create(user=self.fan, post=self.post)
        url = f'/posts/{self.post.id}/unlike/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.filter(user=self.fan, post=self.post).exists())

    def test_cannot_like_twice(self):
        # First like
        Like.objects.create(user=self.fan, post=self.post)
        # Try liking again
        url = f'/posts/{self.post.id}/like/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # -------------------
    # Notification tests
    # -------------------
    def test_notification_created_on_like(self):
        url = f'/posts/{self.post.id}/like/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if notification exists for the author
        self.assertTrue(Notification.objects.filter(
            recipient=self.author,
            actor=self.fan,
            verb="liked your post",
            target_id=self.post.id
        ).exists())

    def test_fetch_notifications(self):
        # Fan likes author's post -> notification should be created
        self.client.post(f'/posts/{self.post.id}/like/')

        # Log in as the author to fetch notifications
        self.client.logout()
        self.client.login(username='author', password='password')

        response = self.client.get('/notifications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify notification is in the response
        self.assertTrue(any("liked your post" in n['verb'] for n in response.data))
