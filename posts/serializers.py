from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_image = serializers.ImageField(source='user.image', default='globalproject/imgs/usr.jpeg')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_image', 'content', 'created_at'] 
