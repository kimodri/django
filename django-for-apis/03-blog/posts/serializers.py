# posts/serializers.py
from rest_framework import serializers 

from .models import Post

from django.contrib.auth import get_user_model

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'author',
            'title',
            'body',
            'created_at',
        )

        model = Post

class UserSerializer(serializers.ModelSerializer):  # new
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
        )