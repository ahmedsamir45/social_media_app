from django.urls import path
from .views import feed, post, usrinfo,add_comment,like_post,dislike_post,search_posts

urlpatterns = [
    path('feed/', feed, name='feed'),
    path('usrinfo/<int:var>/', usrinfo, name='usrinfo'),
    path('feed/post/<int:var>/', post, name='post'),
        path('search/', search_posts, name='search_posts'),
 path('api/add_comment/<int:post_id>/', add_comment, name='add_comment'),
  path('api/like/<int:post_id>/', like_post, name='like_post'),
    path('api/dislike/<int:post_id>/', dislike_post, name='dislike_post'),
]
