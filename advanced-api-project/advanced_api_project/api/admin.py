from django.contrib import admin
from .models import Author, Book

# Register your models here.
# Register the Author model with the admin site
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Register the Book model with the admin site
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    list_filter = ('author',)
    search_fields = ('title',)