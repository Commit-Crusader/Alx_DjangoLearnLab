from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from .models import Post, Comment, Category, Tag

class UserRegisterForm(UserCreationForm):
    """
    Custom user registration form with email field.
    
    Extends Django's built-in UserCreationForm to include email field
    and adds Bootstrap styling for consistent UI appearance.
    
    Attributes:
        email: EmailField for user email address (required)
    
    Usage:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
    """
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to form fields for styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
    
    def save(self, commit=True):
        """
        Save the user with email address.
        
        Args:
            commit (bool): Whether to save to database immediately
            
        Returns:
            User: The created user instance with email set
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class TagWidget(forms.TextInput):
    """
    Custom widget for tag input with enhanced functionality.
    
    Provides real-time tag preview and styling for comma-separated tag input.
    Includes JavaScript for interactive tag management.
    
    Features:
        - Real-time tag preview as badges
        - Bootstrap styling
        - Comma-separated input handling
    """
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control tag-input',
            'placeholder': 'Enter tags separated by commas...',
            'data-role': 'tagsinput'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        """
        Render the tag input widget with JavaScript enhancements.
        
        Args:
            name: Field name
            value: Current field value
            attrs: HTML attributes
            renderer: Form renderer
            
        Returns:
            SafeString: HTML with embedded JavaScript for tag preview
        """
        html = super().render(name, value, attrs, renderer)
        
        # Add JavaScript for tag suggestions and styling
        js = """
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            const tagInput = document.querySelector('[data-role="tagsinput"]');
            if (tagInput) {
                // Add tag styling and functionality
                tagInput.addEventListener('input', function(e) {
                    const value = e.target.value;
                    const tags = value.split(',').map(tag => tag.trim()).filter(tag => tag);
                    
                    // Create tag badges preview
                    let previewHtml = '<div class="tag-preview mt-2">';
                    tags.forEach(tag => {
                        previewHtml += `<span class="badge bg-primary me-1">${tag}</span>`;
                    });
                    previewHtml += '</div>';
                    
                    // Remove existing preview
                    const existingPreview = e.target.parentNode.querySelector('.tag-preview');
                    if (existingPreview) {
                        existingPreview.remove();
                    }
                    
                    // Add new preview if tags exist
                    if (tags.length > 0) {
                        e.target.parentNode.insertAdjacentHTML('beforeend', previewHtml);
                    }
                });
                
                // Trigger initial preview
                tagInput.dispatchEvent(new Event('input'));
            }
        });
        </script>
        """
        return mark_safe(html + js)

class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts with tag support.
    
    Handles post creation/editing including title, content, category selection,
    and tag management through comma-separated string input.
    
    Features:
        - Automatic tag creation from comma-separated strings
        - Category selection with dropdown
        - Bootstrap styling
        - Tag preview functionality
    
    Usage:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()  # Tags are automatically handled
    """
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select a category...",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tags = forms.CharField(
        required=False,
        widget=TagWidget(),
        help_text="Enter tags separated by commas (e.g., python, django, web)"
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your blog post content here...',
                'rows': 10
            })
        }
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the form with custom setup.
        
        Sets up field labels and populates tags field when editing existing posts.
        """
        super().__init__(*args, **kwargs)
        # Add labels
        self.fields['title'].label = 'Post Title'
        self.fields['content'].label = 'Content'
        self.fields['category'].label = 'Category'
        self.fields['tags'].label = 'Tags'
        
        # If editing an existing post, populate tags field
        if self.instance and self.instance.pk:
            self.fields['tags'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])
    
    def save(self, commit=True):
        """
        Save the post and handle tag assignment.
        
        Processes comma-separated tag string into Tag objects and assigns them
        to the post. Creates new tags as needed using get_or_create.
        
        Args:
            commit (bool): Whether to save to database immediately
            
        Returns:
            Post: The saved post instance with tags assigned
            
        Process:
            1. Save the post instance
            2. Parse comma-separated tag string
            3. Create or retrieve Tag objects for each tag name
            4. Assign tags to the post
            5. Clear tags if no tags provided
        """
        post = super().save(commit=False)
        
        if commit:
            post.save()
            
            # Handle tags
            tag_string = self.cleaned_data.get('tags', '')
            if tag_string:
                # Parse comma-separated tag string
                tag_names = [tag.strip() for tag in tag_string.split(',') if tag.strip()]
                
                # Create or get tags and set them
                tags = []
                for tag_name in tag_names:
                    # Use get_or_create to avoid duplicate tags
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    tags.append(tag)
                
                # Assign tags to post using set() for proper many-to-many handling
                post.tags.set(tags)
            else:
                # Clear all tags if none provided
                post.tags.clear()
        
        return post


class CommentForm(forms.ModelForm):
    """
    Form for creating and editing comments on blog posts.
    
    Provides a simple textarea for comment content with validation
    for minimum length requirements.
    
    Features:
        - Bootstrap styling
        - Minimum length validation (5 characters)
        - Character limit (1000 characters)
    
    Usage:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # Associate with post
            comment.save()
    """
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your comment here...',
            'required': True
        }),
        label='Comment',
        max_length=1000
    )
    
    class Meta:
        model = Comment
        fields = ['content']
    
    def clean_content(self):
        """
        Validate comment content for minimum length.
        
        Returns:
            str: Cleaned content
            
        Raises:
            ValidationError: If content is too short
        """
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 5:
            raise forms.ValidationError("Comment must be at least 5 characters long.")
        return content
