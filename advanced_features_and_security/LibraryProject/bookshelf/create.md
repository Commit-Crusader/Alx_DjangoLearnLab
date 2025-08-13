from bookshelf.models import Book

book_one = Book.objects.create(title="1984", author= "George Orwell", publication_year= "1949")
