from django import forms

class ExampleForm(forms.Form):
    title = forms.CharField(max_length=100, label="Book Title")
    author = forms.CharField(max_length=100, label="Author Name")
    description = forms.CharField(widget=forms.Textarea, label="Description")
