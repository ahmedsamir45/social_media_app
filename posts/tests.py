from django.test import TestCase

# Create your tests here.
"""
from django.shortcuts import render
from .models import Post
from userapp.models import CustomUser  # Adjust this import based on your user model location

def feed(request):
    posts = Post.objects.all()  # Get all posts for the feed
    return render(request, "posts/feed.html", {"posts": posts})

def usrinfo(request, var):
    user = CustomUser.objects.get(id=var)  # Fetch user based on var (user ID)
    return render(request, "posts/usrinfo.html", {"user": user})

def post(request, var):
    post_instance = Post.objects.get(id=var)  # Fetch post based on var (post ID)
    return render(request, "posts/post.html", {"post": post_instance})

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Post, Comment


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
            'content': comment.content
        })
    
    return JsonResponse({'success': False}, status=400)

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Post

@login_required
@require_POST
def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return JsonResponse({'success': True, 'count': post.likes.count()})

@login_required
@require_POST
def dislike(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
    return JsonResponse({'success': True, 'count': post.dislikes.count()})









    from django.urls import path
from .views import feed, post, usrinfo, add_comment
from django.urls import path
from .views import post, add_comment, like, dislike
urlpatterns = [
    path('feed/', feed, name='feed'),
    path('usrinfo/<int:var>/', usrinfo, name='usrinfo'),
    path('feed/post/<int:var>/', post, name='post'),
    path('api/add_comment/<int:post_id>/', add_comment, name='add_comment'),
     path('feed/post/<int:var>/', post, name='post'),
    path('api/add_comment/<int:post_id>/', add_comment, name='add_comment'),
    path('api/like/<int:post_id>/', like, name='like'),
    path('api/dislike/<int:post_id>/', dislike, name='dislike'),
]


"""