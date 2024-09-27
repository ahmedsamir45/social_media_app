from django.db import models
from django.utils import timezone
from userapp.models import CustomUser  # Adjust this import based on your user model location

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True, default='globalproject/imgs/usr.jpeg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(CustomUser, related_name='disliked_posts', blank=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Post - {self.created_at}"

    def like_count(self):
        return self.likes.count()

    def dislike_count(self):
        return self.dislikes.count()

    def comment_count(self):
        return self.comments.count()

    def is_recent(self):
        return timezone.now() - self.created_at <= timezone.timedelta(hours=24)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"

    def is_recent(self):
        return timezone.now() - self.created_at <= timezone.timedelta(hours=1)