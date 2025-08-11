from django.urls import path, include
from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView



urlpatterns = {
        path('listbooks/', views.list_books, name=listbooks),
        path('librarydetail/', views.LibraryDetailView, name=librarydetailview)
        path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login')
        path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout')
        path('register/', views.register.as_view(), name='register')
