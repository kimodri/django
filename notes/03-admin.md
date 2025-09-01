# 💪🏿 Django Admin
- For context we are still doing the message board application here and it has an app called `posts`
This is an application interface that let's the admin interract with the data and to do that
- create a `superuser` who can login
```shell
(.venv) > python manage.py createsuperuser
Username (leave blank to use 'wsv'): wsv
Email: will@wsvincent.com
Password:
Password (again):
Superuser created successfully.
```
Visit the admin through:

`http://127.0.0.1:8000/admin/` here you will see:
![admin page](../assets/admin.jpeg)
- **NOTE** You won't see your apps here untill you edit the `app`'s `admin.py` file
```python
# posts/admin.py
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```
In the admin page, you can see the `instances` or `objects` of your model, to make them descriptive, use either:
![admin-posts-object](../assets/admin-post-object.jpeg)
- `def __str__(self):`
- `def __repr__(self):`
In your class (table)