from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/',  auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # Profile URLs
    path('profile/', views.profile, name='profile'),  # view & edit
    # Home page
    path('home', views.home, name='home'),
    path('', views.home, name='home'),
    # Posts
    path('posts/', views.posts, name='posts'),
]
