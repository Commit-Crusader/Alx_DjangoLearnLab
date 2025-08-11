from django.urls import path, include
from .views import list_books, LibraryDetailView



urlpatterns = {
        path('listbooks/', views.list_books, name=listbooks),
        path('librarydetail/', views.LibraryDetailView, name=librarydetailview)

