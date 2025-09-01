# Django's Tests
Django has its own testing framework **on top of** Python's `unittest.TestCase` base class, this includes:
- `test client`: Making dummy web browser requests
- `SimpleTestCase`: used when a database is not necessary
- `TestCase`: used when you do want to test the database
- `TransactionTestCase`: useful if you need to directly test the `database transactions`
- `LiverServerTestCase`: launches a liver server thread useful for testing with browser-based tools like Selenium

## Checking the URL response only
If you just want to check if the `url`s you registered return HTTP status codes of 200, you can do:
```python
# pages/tests.py
from django.test import SimpleTestCase
 
class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
 
class AboutpageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
```
To run it:

`python manage.py test`

## Checking the `name` of the pages
Remember that in `urls.py` from `app` folder we specify the name of the view, we can check that by doing:

```python
from django.test import SimpleTestCase
from django.urls import reverse

class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
    
    def test_url_available_by_name(self): # new
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

class AboutpageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
        
     def test_url_available_by_name(self): # new
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

```
## `TestCase`
For when you are testing with a database
- This will let us create a test database we can check against
- We don't need to run tests on our actual database but instead make a spearate database, fill it with sample data, and test against it

### `setUpTestData()`
- Used to create our test data

### Testing with a database
- Our app is called `posts` it has a database with only one model called `Post` with a single field called `text`
```python
# posts/tests.py
from django.test import TestCase
from .models import Post

class PostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(text="This is a test!")

    def test_model_content(self):
        self.assertEqual(self.post.text, "This is a test!")
```
- We import the TestCase and our model: Post
- We create a test class: PostTests that extends TestCase
- We use the built in `setUpTestData`
- In this instance, we only have one item stored as `cls.post` that can then be referred to in any subsequent tests within the class as `self.post`. 
- If you run this only the function with the `test_...` will run other functions are helper functions
