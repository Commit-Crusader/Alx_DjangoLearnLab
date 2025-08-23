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
    
    # Posts URLs - using class-based views
    path('posts/', views.ListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.DetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.UpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.DeleteView.as_view(), name='post_delete'),

    # Comments URLs
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comments/', views.CommentListView.as_view(), name='comment_list'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]
