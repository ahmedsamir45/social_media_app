# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views import View
from .forms import CustomUserCreationForm

# Use the custom user model
User = get_user_model()

# Register View
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately after registration
            return redirect('login')  # Redirect to 'feeds' or a main page after registration
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'userapp/register.html', {'form': form})


# Login View
class LoginView(View):
    def get(self, request):
        return render(request, 'userapp/login.html')

    def post(self, request):
        # Safely get email and password to avoid potential KeyErrors
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, "Both email and password are required.")
            return render(request, 'userapp/login.html')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to the desired page after successful login
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "No user found with this email address.")
        
        return render(request, 'userapp/login.html')



from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from posts.models import Post,Comment  # Import your Post and Comment models

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from posts.models import Post  # Import your Post model

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from posts.models import Post  # Import your Post model

@login_required
def dashboard(request):
    user = request.user  # Get the currently logged-in user
    posts = Post.objects.filter(user=user)  # Get all posts by the user
    
    if request.method == "POST":
        content = request.POST.get('post')
        image = request.FILES.get('img')  # Handle image upload
        # Create a new post using 'user' to match the model
        Post.objects.create(user=user, content=content, image=image)
        return redirect('dashboard')  # Redirect to the dashboard after posting

    return render(request, 'userapp/dashboard.html', {'user': user, 'posts': posts})

from django.contrib.auth import logout
def logout_view(request):
    logout(request)  # Log the user out
    messages.success(request, "You have successfully logged out.")
    return redirect('landing')  # Redirect to the landing page after logout
