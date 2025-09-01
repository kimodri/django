# 🫙 Databases
The only configuration required when working with a database is the `DATABASES` section of our `django_project/settings.py`
- For context, the book is creating a message board app

## Create a Database Model
To create a model, open the `<app>/models.py`:
```python
# posts is the name of the app
# posts/models.py
from django.db import models

class Post(models.Model):
    text = models.TextField()
```

## Activate Models
Whenever we create or modify an existing model we'll need to update Django in a _two-step process_:
1. We create a migration file with the `makemigrations` command
2. We build the actual database with the `migrate` command which executes the instructions on our migrations file

```shell
(.venv) > python manage.py makemigrations posts
Migrations for 'posts':
    posts/migrations/0001_initial.py
        - Create model Post

(.venv) > python manage.py migrate
Operations to perform:
    Apply all migrations: admin, auth, contenttypes, posts, sessions
Running migrations:
    Applying posts.0001_initial... OK
```
- Therefore, as a best practice, adopt the habit of always including the name of an app when executing the makemigrations command!
- If you just `makemigrations` all the models inside the app will create migration file
