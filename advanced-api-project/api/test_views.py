# api/test_views.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Author, Book

class BookAPITestCase(APITestCase):
    """
    Test suite for Book API endpoints
    Tests CRUD operations, permissions, and filtering
    """
    
    def setUp(self):
        """
        Set up test data before each test method
        This runs before EVERY test method
        """
        # Create test user for authentication
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test author
        self.author = Author.objects.create(name='Test Author')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Test Book 1',
            publication_year=2020,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title='Another Book',
            publication_year=2021,
            author=self.author
        )
        
        # Set up API client
        self.client = APIClient()
    
    def test_get_book_list(self):
        """Test retrieving list of all books"""
        url = reverse('book-list')  # /api/books/
        response = self.client.get(url)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response data
        self.assertEqual(len(response.data), 2)  # Should have 2 books
    
    def test_get_single_book(self):
        """Test retrieving a single book by ID"""
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book 1')
    
    def test_get_nonexistent_book(self):
        """Test retrieving a book that doesn't exist"""
        url = reverse('book-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_book_authenticated(self):
        """Test creating a book with authentication"""
        # Login the user
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Test Book')
        
        # Verify book was actually created in database
        self.assertTrue(Book.objects.filter(title='New Test Book').exists())
    
    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication (should fail)"""
        url = reverse('book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify book was NOT created
        self.assertFalse(Book.objects.filter(title='Unauthorized Book').exists())
    
    def test_update_book_authenticated(self):
        """Test updating a book with authentication"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-update')
        data = {
            'id': self.book1.id,
            'title': 'Updated Book Title',
            'publication_year': 2022,
            'author': self.author.id
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book Title')
    
    def test_update_book_unauthenticated(self):
        """Test updating a book without authentication (should fail)"""
        url = reverse('book-update')
        data = {
            'id': self.book1.id,
            'title': 'Unauthorized Update',
            'publication_year': 2022,
            'author': self.author.id
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_book_authenticated(self):
        """Test deleting a book with authentication"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-delete')
        data = {'id': self.book1.id}
        
        response = self.client.delete(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify book was deleted
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
    
    def test_delete_book_unauthenticated(self):
        """Test deleting a book without authentication (should fail)"""
        url = reverse('book-delete')
        data = {'id': self.book1.id}
        
        response = self.client.delete(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify book still exists
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())
    
    def test_filter_books_by_title(self):
        """Test filtering books by title"""
        url = reverse('book-list')
        response = self.client.get(url, {'title': 'Test'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return only books with "Test" in title
        self.assertEqual(len(response.data), 1)
    
    def test_search_books(self):
        """Test searching books across title and author"""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Another'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_order_books_by_title(self):
        """Test ordering books by title"""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # First book should be "Another Book" (alphabetically first)
        self.assertEqual(response.data[0]['title'], 'Another Book')
    
    def test_create_book_invalid_data(self):
        """Test creating a book with invalid data"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-create')
        # Missing required fields
        data = {
            'title': '',  # Empty title
            'publication_year': 2025,  # Future year (should fail validation)
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)