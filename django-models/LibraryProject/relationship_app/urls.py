from django.urls import path, include
from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from . import views



urlpatterns = [
        path('list_books/', views.list_books, name='list_books'),
        path('LibraryDetailView/', views.LibraryDetailView.as_view(), name='LibraryDetailView'),
        path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
        path('logout/', LogoutView.as_view(), name='logout'),
        path('register/', views.register_view, name='register'),

        ]
