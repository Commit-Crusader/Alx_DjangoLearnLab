from django.test import TestCase
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="J.K. Rowling")

    def test_author_creation(self):
        self.assertEqual(self.author.name, "J.K. Rowling")

class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter and the Philosopher's Stone", publication_year=1997, author=self.author)

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Harry Potter and the Philosopher's Stone")
        self.assertEqual(self.book.publication_year, 1997)
        self.assertEqual(self.book.author.name, "J.K. Rowling")

class BookSerializerTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter and the Philosopher's Stone", publication_year=1997, author=self.author)
        self.serializer = BookSerializer(instance=self.book)

    def test_book_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['title'], "Harry Potter and the Philosopher's Stone")
        self.assertEqual(data['publication_year'], 1997)
        self.assertEqual(data['author'], self.author.id)

    def test_publication_year_validation(self):
        invalid_book = Book(title="Future Book", publication_year=2025, author=self.author)
        serializer = BookSerializer(instance=invalid_book)
        self.assertFalse(serializer.is_valid())
        self.assertIn('publication_year', serializer.errors)

class AuthorSerializerTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter and the Philosopher's Stone", publication_year=1997, author=self.author)
        self.serializer = AuthorSerializer(instance=self.author)

    def test_author_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['name'], "J.K. Rowling")
        self.assertEqual(len(data['books']), 1)
        self.assertEqual(data['books'][0]['title'], "Harry Potter and the Philosopher's Stone")
