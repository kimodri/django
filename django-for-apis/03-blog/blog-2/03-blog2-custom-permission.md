# Custom Permissions
A scenario could be if we want to restrict access so that only the author of a blog post can edit it or delete it.
- The admin superuser will have access to do everything but a regular user can only update/delete their own content

## Context
Django REST Framework relies on a BasePermission class from which all other permission classes inherit. All the built-in permissions settings like `AllowAny` or `IsAuthenticated` simple extend `BasePermission`

```python
class BasePermission(object): 
    """ 
    A base class from which all permission classes should inherit. 
    """ 

    def has_permission(self, request, view):

        """ 
        Return `True` if permission is granted, `False` otherwise. 
        """ 
        return True

    def has_object_permission(self, request, view, obj): 
        
        """ 
        Return `True` if permission is granted, `False` otherwise. 
        """ 
        return True
```
For a custom permission class you can override one or both of these methods. 
- `has_permission` works on list views 
- **detail views** execute both: first `has_permission` and then, if that passes, `has_object_permission`. 
- It is strongly advised to always set both methods explicitly because each defaults to True, meaning they will allow access implicitly unless set explicitly.

## What we want
- Remember that we want only the author of a blog post to have write permissions to edit or delete it
- We also want to restrict read-only list view to authenticated users.

## Customizing
To get started create a file: `posts/permissions.py`
```python
from rest_framework import permissions

# we are creating our own permission here just like "isAuthenticatedOnly"
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        
        # authenticated users only can see list view
        if request.user.is_authenticated:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request so we'll always
        # GET, HEAD, or OPTIONS requests

        if request.method in permissions.SAFE_METHODS:
            return True
        
        # the object that we are pertaining here is the object/instance of the mode
        # hence if we have a class view and we have this as the value of the permission_classes
        # it will require a model
        return obj.author == request.user  # if the same this will be true
```
- The first methos `has_permission` requires that a user be logged in or authenticated
- The second allows read only requests but limits write permissions to only the author of the blog post

- We access the author field via obj.author and the current user with request.user.

Now that you have another permission you can edit your view-level permission
```python
# posts/views.py
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Post
from .permissions import IsAuthorOrReadOnly

from .serializers import PostSerializer

class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadOnly, )  # new
    queryset = Post.objects.all() 
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly, )  # new
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```
