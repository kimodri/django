from django.shortcuts import render
from django.contrib.auth import get_user_model  # new
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser # new

# Create your views here.
# from rest_framework import generics
from .models import Post
from .permissions import IsAuthorOrReadOnly

from .serializers import PostSerializer, UserSerializer

# class PostList(generics.ListCreateAPIView):
#     permission_classes = (IsAuthorOrReadOnly, )  # new
#     queryset = Post.objects.all() 
#     serializer_class = PostSerializer

# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsAuthorOrReadOnly, )  # new
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class UserList(generics.ListCreateAPIView):
#     queryset = get_user_model().objects.all()
#     serializer_class = UserSerializer

# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = get_user_model().objects.all()
#     serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer




