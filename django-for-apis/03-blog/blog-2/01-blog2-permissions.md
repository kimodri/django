We have a problem from last blog app, and that is anyone can edit/delete/add a post!

# Permissions
DRF ships with several permission settings that we can use to secure our API, applicable at:
- project-level
- view-level
- any _individual_ model level

What we want to do is end up with a custom persmissions so that only the author of a blog has the ability to update or delete it

## Project-Level Permissions
At this time all we have been doing is:
```python
# django_project/settings.py 
REST_FRAMEWORK = { 
        "DEFAULT_PERMISSION_CLASSES": [ 
                "rest_framework.permissions.AllowAny",  # new 
            ], 
    } 
```
### Four Built in PL Permissions
- `AllowAny` - any user, authenticated or not, has full access
- `IsAuthenticated` - only authenticated, registered users have access
- `IsAdminUser` - only admins/superusers have access
- `IsAuthenticatedOrReadOnly` - unauthorized users can view any page, but only authenticated users have write, edit, or delete privileges

Implementing any of these four settings requires updating the `DEFAULT_PERMISSION_CLASSES` setting and refreshing our web browser.

If changed the permission to `IsAuthenticated`, now running the `blog_request.py` will return

`{'detail': 'Authentication credentials were not provided.'}`

## View-Level Permissions
Permissions can be added at the view for example if you want the admin to be just the one to see the `PostDetail` then  a logged out user can’t view the API at all, a logged-in user can view the list page, but only an admin can see the detail page.

```python
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Post

from .serializers import PostSerializer

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all() 
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser, )  # new
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```