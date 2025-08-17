from django.db import models

class Author(models.Model):
    """
    Author model represents book authors
    Each author can have multiple books (one-to-many relationship)
    """
    
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    """
    Book model represents books written by authors
    Each book is linked to one author (many-to-one relationship)
    """
    
    title = models.CharField(max_length=200)
    #Foreign Key creates a many-to-one relationship with Author
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    publication_year =models.IntegerField()
    def __str__(self):
        return self.title
