from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/',  auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),

    # Profile URLs
    path('profile/', views.profile_view, name='profile'),  # view & edit
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    
    # Home page
    path('', views.home_view, name='home'),
    
    # Posts URLs
    path('posts/', views.post_list_view, name='post_list'),
    path('posts/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('posts/create/', views.create_post_view, name='create_post'),
    path('posts/<int:post_id>/edit/', views.edit_post_view, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
]
