from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'isbn']

    def clean_isbn(self):
        """Validate ISBN format"""
        isbn = self.cleaned_data['isbn']
        if not isbn.isdigit() or len(isbn) != 13:
            raise forms.ValidationError("ISBN must be 13 digits")
        return isbn

    def clean_title(self):
        """Sanitize title field"""
        title = self.cleaned_data['title']
        # Remove potentially dangerous characters
        return forms.utils.strip_tags(title)