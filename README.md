# UR Social

## Table of Contents
- [Introduction](#introduction)
- [Team Members](#team-members)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [Use Cases](#use-cases)
- [API Endpoints](#api-endpoints)
- [Setup Instructions](#setup-instructions)

## Introduction
This project is a social media application built using Django. It allows users to register, create posts, comment on posts, and like or dislike posts. The frontend is built using HTML, CSS, and JavaScript, while the backend is powered by Django and Django REST framework.

## Team Members
- [Mohamed Osama](https://github.com/mohamedosama12345/)
- [Ahmed Samir](https://github.com/ahmedsamir45)
- Mohamed Mahmoud

## Technologies Used
- **Backend**: Django, Django REST framework
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Other**: jQuery

## Project Structure
```
db.sqlite3
front end/
    about.html
    contact.html
    dashboard.html
    feed.html
    index.html
    login.html
    post.html
    register.html
    usrinfo.html
global/
    models.py
    urls.py
    views.py
media/
    posts/
    profile_images/
posts/
    serializers.py
    views.py
social_media_app/
    settings.py
    urls.py
    wsgi.py
userapp/
    models.py
    serializers.py
    views.py
```

## Database Models

### CustomUser
Defined in `userapp/migrations/0001_initial.py`:
```py
class CustomUser(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    password = models.CharField(max_length=128, verbose_name='password')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='last login')
    is_superuser = models.BooleanField(default=False, verbose_name='superuser status')
    username = models.CharField(max_length=150, unique=True, verbose_name='username')
    is_staff = models.BooleanField(default=False, verbose_name='staff status')
    is_active = models.BooleanField(default=True, verbose_name='active')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='date joined')
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='profile_images/')
    birth_date = models.DateField(default=datetime.date.today)
    registration_date = models.DateField(auto_now_add=True)
    first_name = models.CharField(blank=True, max_length=30)
    last_name = models.CharField(blank=True, max_length=150)
    groups = models.ManyToManyField(blank=True, to='auth.group', verbose_name='groups')
    user_permissions = models.ManyToManyField(blank=True, to='auth.permission', verbose_name='user permissions')
```

### Post
Defined in `posts/models.py`:
```py
class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(CustomUser, related_name='disliked_posts', blank=True)
    class Meta:
        ordering = ['-created_at']
```

### Comment
Defined in `posts/models.py`:
```py
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['created_at']
```

## Use Cases
1. **User Registration**: Users can register with a unique username and email.
2. **User Login**: Registered users can log in to the application.
3. **Create Post**: Logged-in users can create new posts with text and optional images.
4. **Comment on Post**: Users can comment on posts.
5. **Like/Dislike Post**: Users can like or dislike posts.
6. **View Feed**: Users can view a feed of all posts.
7. **User Profile**: Users can view their profile and other users' profiles.

## API Endpoints

### Add Comment
Defined in `posts/views.py`:
```py
@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment_content = request.POST.get('content')
    if comment_content:
        comment = Comment.objects.create(user=request.user, post=post, content=comment_content)
        return JsonResponse({
            'success': True,
            'user_id': comment.user.id,
            'username': comment.user.username,
            'content': comment.content,
            'image': comment.user.image.url if comment.user.image else None,
            'count_comment': post.comments.count()
        })
    return JsonResponse({'success': False}, status=400)
```

### Like Post
Defined in `posts/views.py`:
```py
@api_view(['POST'])
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        post.dislikes.remove(user)
        liked = True
    return Response({
        'success': True,
        'count': post.likes.count(),
        'disliked_count': post.dislikes.count(),
        'liked': liked
    }, status=status.HTTP_200_OK)
```

### Dislike Post
Defined in `posts/views.py`:
```py
@api_view(['POST'])
def dislike_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    if user in post.dislikes.all():
        post.dislikes.remove(user)
        disliked = False
    else:
        post.dislikes.add(user)
        post.likes.remove(user)
        disliked = True
    return Response({
        'success': True,
        'count': post.dislikes.count(),
        'liked_count': post.likes.count(),
        'disliked': disliked
    }, status=status.HTTP_200_OK)
```

## Setup Instructions

1. **Clone the repository**:
    ```sh
    git clone https://github.com/ahmedsamir45/social_media_app.git
    cd <repository-directory>
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Apply migrations**:
    ```sh
    python manage.py migrate
    ```

4. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

5. **Access the application**:
    Open your browser and navigate to `http://127.0.0.1:8000/`.