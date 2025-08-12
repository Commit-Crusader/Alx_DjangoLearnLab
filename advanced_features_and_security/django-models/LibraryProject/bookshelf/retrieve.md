# Retrieve md

from bookshelf.models import Book

book = Book.objects.get(title="1984")

print(book.title)
print(book.author)
print(book.publication_year)
