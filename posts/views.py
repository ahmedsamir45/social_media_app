from django.shortcuts import render
from .models import Post
from userapp.models import CustomUser  # Adjust this import based on your user model location
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post

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


from django.shortcuts import render
from .models import Post, Comment
from userapp.models import CustomUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# ... (existing feed, usrinfo, and post views)
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Post, Comment

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment_content = request.POST.get('content')

    if comment_content:
        comment = Comment.objects.create(user=request.user, post=post, content=comment_content)
        
        # Ensure the image field is serialized properly
        user_image = comment.user.image.url if comment.user.image else None  # Use .url to get the image URL
        comment_count = post.comments.count()
        
        return JsonResponse({
            'success': True,
            'user_id': comment.user.id,
            'username': comment.user.username,
            'content': comment.content,
            'image': user_image,  # Ensure this is a URL or None
            "count_comment":int(comment_count)
        })
    
    return JsonResponse({'success': False}, status=400)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post

@api_view(['POST'])
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    if user in post.likes.all():
        # User already liked the post, so remove the like
        post.likes.remove(user)
        liked = False
    else:
        # User hasn't liked the post, so add the like and remove dislike if present
        post.likes.add(user)
        post.dislikes.remove(user)
        liked = True

    return Response({
        'success': True,
        'count': post.likes.count(),  # Current like count
        'disliked_count': post.dislikes.count(),  # Include dislike count
        'liked': liked
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def dislike_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    if user in post.dislikes.all():
        # User already disliked the post, so remove the dislike
        post.dislikes.remove(user)
        disliked = False
    else:
        # User hasn't disliked the post, so add the dislike and remove like if present
        post.dislikes.add(user)
        post.likes.remove(user)
        disliked = True

    return Response({
        'success': True,
        'count': int(post.dislikes.count()),  # Current dislike count
        'liked_count': int(post.likes.count()),  # Include like count
        'disliked': disliked
    }, status=status.HTTP_200_OK)
from django.shortcuts import render
from .models import Post

from django.shortcuts import render
from django.db.models import Q
from .models import Post

def search_posts(request):
    query = request.GET.get('query', '')  # Get the search query from the URL
    if query:
        # Search in post content, title, and author's username fields
        results = Post.objects.filter(
            Q(content__icontains=query) |
            Q(user__username__icontains=query)  # Adjusted for the `user` relation instead of `author`
        )
    else:
        results = Post.objects.none()  # No results if no query provided

    return render(request, 'posts/search_results.html', {'query': query, 'results': results})
