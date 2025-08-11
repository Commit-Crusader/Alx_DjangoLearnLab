from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    #Create sample data for testing queries

    #Create Authors

    author1 = Author.object.create(name = 'J.K. Rowling')
    author2 = Author.object.create(name = 'George Orwell')

    #Create Books

    book1 = Book.object.create(title = 'Harry Potter', author = author1)
    book2 = Book.object.create(title = '1984', author = author2)

    #Create Library

    library = Library.object.create(name = 'Light House')
    library.books.add(book1, book2)

    #Create Librarian

    librarian = Librarian.object.create(name = 'Susan', library = library)

    print("Sample data added successfully")


def query_books_by_author():
    """Query all books by a specific author (ForeignKey relationship)"""
    
    author_name = "J.K. Rowling"
    author = Author.objects.get(name=author_name)
    
    # Get all books by this author
    books = Book.objects.filter(author=author)
    
    print(f"\nBooks by {author_name}:")
    for book in books:
        print(f"- {book.title}")

def query_books_in_library():
    """List all books in a library (ManyToMany relationship)"""
    
    library_name = "Central Library"
    library = Library.objects.get(name=library_name)
    
    # Get all books in this library
    books = library.books.all()
    
    print(f"\nBooks in {library_name}:")
    for book in books:
        print(f"- {book.title} by {book.author.name}")

def query_librarian_for_library():
    """Retrieve the librarian for a library (OneToOne relationship)"""
    
    library_name = "Light House"
    library = Library.objects.get(name=library_name)
    
    # Get librarian for this library
    librarian = library.librarian
    
    print(f"\nLibrarian for {library_name}: {librarian.name}")

# Run all functions
if __name__ == "__main__":
    print("Creating sample data...")
    create_sample_data()
    
    print("\n" + "="*50)
    print("RUNNING SAMPLE QUERIES")
    print("="*50)
    
    query_books_by_author()
    query_books_in_library()
    query_librarian_for_library()
