from django.urls import path, include
from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from . import views



urlpatterns = [
        path('list_books/', views.list_books, name='list_books'),
        path('LibraryDetailView/', views.LibraryDetailView.as_view(), name='LibraryDetailView'),
        path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
        path('logout/', LogoutView.as_view(), name='logout'),
        path('register/', views.register.as_view(), name='register'),
        path('admin-dashboard/', views.admin_view, name='admin_view'),
        path('librarian/', views.librarian_view, name='librarian_view'),
        path('member/', views.member_view, name='member_view'),
        # Book management views with permissions
        path('books/', views.list_books, name='list_books'),
        path('books/add/', views.add_book, name='add_book'),
        path('books/edit/<int:pk>/', views.edit_book, name='edit_book'),
        path('books/delete/<int:pk>/', views.delete_book, name='delete_book'),
]
