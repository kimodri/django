# Posts App
After handling the users, it is now time to create a dedictead app for the blog

- We assume that you have created a new app called `posts`
- Added in the `INSTALLED_APPS` in `django_project/settings.py`

1. Crete a Post Complex Model
- We will also create a model:
```python
from django.db import models
from django.conf import settings
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at =  models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```
2. Update `posts/admin.py` so the model will show
```python
from django.contrib import admin
from .models import Post

# Register your models here.
admin.site.register(Post)
```
3. Test
```python
from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.
from .models import Post

class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )

        cls.post = Post.objects.create(
            author=cls.user,
            title="A good title",
            body="Nice body content",
        )

    def test_post_model(self):
        self.assertEqual(self.post.author.username, "testuser") 
        self.assertEqual(self.post.title, "A good title") 
        self.assertEqual(self.post.body, "Nice body content") 
        self.assertEqual(str(self.post), "A good title") 
``` 