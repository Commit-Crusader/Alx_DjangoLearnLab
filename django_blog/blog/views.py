from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Post

def register_view(request):
    """
    Handle user registration
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save()
            # Log the user in automatically after registration
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')  # Redirect to profile page
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile_view(request):
    """
    Display user profile page - requires login
    """
    return render(request, 'blog/profile.html', {'user': request.user})

@login_required
def edit_profile_view(request):
    """
    Allow users to edit their profile information
    """
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        
        # Update user information
        user = request.user
        user.email = email
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'blog/edit_profile.html', {'user': request.user})