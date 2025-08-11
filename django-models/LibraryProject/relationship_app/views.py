from django.shortcuts import render

# Create your views here.


def list_books(request):
    books = book.objects.all()
    context = {'book_list': books}
    return render(request, 'relationship_app/list_books.html', context)
