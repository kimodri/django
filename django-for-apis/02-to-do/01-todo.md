1. Create an endpoint for all todos and specific
2. Cross-origin Resource Sharing (CORS) a security feature whena a deployed back-end needs to communicate with a front-end

Assume that you already have a project called `django_project` and an app called `todos` and that the database has been migrated and that you also have a model:
```python
from django.db import models

# Create your models here.
class Todo(models.Models):
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title
```
- Remember `makemigrations` and `migrate`
- Assume also that you have created an admin
- We assume also that you have written a test for your database:
```python
# todos/tests.py 
from django.test import TestCase 
from .models import Todo 

class TodoModelTest(TestCase): 
    @classmethod 
    def setUpTestData(cls): 
        cls.todo = Todo.objects.create( 
                title="First Todo", 
                body="A body of text here" 
            ) 
        
def test_model_content(self): 
    self.assertEqual(self.todo.title, "First Todo") 
    self.assertEqual(self.todo.body, "A body of text here") 
    self.assertEqual(str(self.todo), "First Todo")
```
## Start of REST
- Add the third party app to the `INSTALLED_APPS` 

### Configuring Rest App 
We configure our third party rest app by adding:
```python
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES":[
        "rest_framework.permissions.AllowAny" # this is bad because this allow any request may it be auth or not
    ],
}
```
- DRF has a list of implicitly default settings and `AllowAny` is one of them
- Remember too that much like the default django its default settings are **not appropriate** for production that's why before deployment we will typically make a number of changes to them

### Edit the URL
1. Start with the project level first:
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("todos.urls"))
]
```
2. Then create the app-level: `todos/urls.py`
```python
from django.urls import path

from .views import ListTodo, DetailTodo

urlpatterns = [
    path("<int:pk>/", DetailTodo.as_view(), name="todo_detail"),
    path("", ListTodo.as_view(), name="todo_list"),
    
]
```
- We are referencing two views that we still have not created 

## Serializers
1. Create a new file  `<app>/serializers.py` file and update it with the following code:
```python
from rest_framework import serializers

from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        Fields = (
            "id",
            "title",
            "body",
        )
``` 
- What we just do here is specifying which model we want to use and specific fields on it we want to expose

## Views
- `ListAPIView` to display all todos
- `RetrieveAPIView` to display a single model instance
```python
from rest_framework import generics

from .models import Todo
from .serializers import TodoSerializer

class ListTodo(generics.ListAPIView):
    queryset = Todo.objetcs.all()
    serializer_class = TodoSerializer

class DetailTodo(generics.RetrieveAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
```

## API Tests
in your `todos/tests.py`:
```python
# add this:
...

class TodoAPITest(APITestCase):

    def setUp(self):
        self.todo = Todo.objects.create(
            title="First Todo",
            body="A body of text here"
        )
    
    def test_api_listview(self):
        response = self.client.get(reverse("todo_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Todo.objects.count(), 1)
        
        # A better way to test the content:
        self.assertEqual(response.data[0]['title'], "First Todo")
        self.assertEqual(response.data[0]['body'], "A body of text here")
        
    def test_api_detailview(self):
        response = self.client.get(
            reverse("todo_detail", kwargs={"pk": self.todo.id}),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Todo.objects.count(), 1)
        
        # A more precise way to check content:
        self.assertEqual(response.data['title'], "First Todo")
        self.assertEqual(response.data['body'], "A body of text here")
``` 