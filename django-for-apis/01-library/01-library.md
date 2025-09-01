# Creating an Endpoint for Library
The goal of this chapter are:
- Create the first ever view that will expose and API endpoint
- List the books in JSON
---
After installing djangorestframework with pip:
1. You have to notify django of the new installation in our `django_project/settings.py`
```python
# django_project/settings.py
INSTALLED_APPS = [
    ...
    'django.contrib.staticfiles',

    # 3rd party apps
    'rest_framework',

    # local apps
    'books.apps.BooksConfig',
]
```
## Creating an API View (Endpoint)
1. Now, developers often include the api logic inside the related app and just have an `api/` prefix but you can also create another app: `apis`:

> `python manage.py startapp apis`

2. With a new app you have to include it in `INSTALLED_APPS`:

```python
# django_project/settings.py
INSTALLED_APPS = [
    ...
    'django.contrib.staticfiles',

    # 3rd party apps
    'rest_framework',

    # local apps
    'books.apps.BooksConfig',
    'apis.apps.ApisConfig', # new
]
```
Since this app will not have its own database there is no need for migrations

3. We'll then need to edit the `url` in the project folder:
```python
# django_project/urls.py 
from django.contrib import admin 
from django.urls import path, include

urlpatterns = [ 
        path("admin/", admin.site.urls), 
        path("api/", include("apis.urls")),  # new 
        path("", include("books.urls")), 
    ] 
```
4. Create a `urls.py` in the api app this will include the views you will create in the `apis/views.py`
```python
# apis/urls.py 
from django.urls import path 
from .views import BookAPIView 

urlpatterns = [ 
        path("", BookAPIView.as_view(), name="book_list"), 
    ] 
```
## Views
Views are used here to customize what data to send in **`JSON`** format
- REST Framework views rely on model, a URL and a new file called a serializer
- DRF have a lot of classes of views for common use cases such as `ListAPIView` to display all
5. Create a view
```python
# apis/views.py 
from rest_framework import generics  # we import the class based views
from books.models import Book  # we import the table Book
from .serializers import BookSerializer  # we import a serializer class that we still haven't made

class BookAPIView(generics.ListAPIView): 
    queryset = Book.objects.all() 
    serializer_class = BookSerializer
```

## Serializers
- A serializer translates complex data like querysets and model instances into a format that is easy to consime over the internet: `JSON`

6. Create a new file called `apis/serializers.py` and update it as follows:
```python
# apis/serializers.py 

from rest_framework import serializers 
from books.models import Book 

    class BookSerializer(serializers.ModelSerializer): 
        class Meta: 
            model = Book 
            fields = ("title", "subtitle", "author", "isbn")
```

## Tests
Django comes with a `test client` that we can use to simulate `GET` or `POST` requests
- DRF provides additional helper classes that extend Django's existing test framework: `APIClient` an extension of Django's default `Client`
    - we want to know that we get `200 OK` and that it contains the correct content
1. Open the `apis/test.py` and have the code:
```python
from rest_framework import status 
from rest_framework.test import APITestCase

from books.models import Book 


class APITests(APITestCase): 
    @classmethod 
    def setUpTestData(cls): 
        cls.book = Book.objects.create( 
            title="Django for APIs", 
            subtitle="Build web APIs with Python and Django", 
            author="William S. Vincent", 
            isbn="9781735467221", 
        )

    def test_api_listview(self): 
        response = self.client.get(reverse("book_list"))  # reverse is for getting the url
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(Book.objects.count(), 1) 
        self.assertContains(response, self.book) 
```
and then run `python manage.py test apis`