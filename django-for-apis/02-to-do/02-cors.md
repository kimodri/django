# CORS
- It is like saying "Where do you allow requests to come from?
- For public API their specified CORS is `*` which means that is allowable by all
- Whenever a client interacts with an API hosted on a different domain or port there are potential security issues
- CORS requires the web server to include specific HTTP headers that allow for the client to determine if and when cross-domain request should be allowed, this includes HTTP verbs

## Handling CORS
- Use middleware that will automatically include the appropriate HTTP headers based on our settings 
1.  `django-cors-headers`
> `python -m pip install django-cors-headers`
2. Update our `django_project/settings.py` in three places:
- add `corsheaders` to the `INSTALLED_APPS`
- add  `CorsMiddleware` above `CommonMiddleWare` in `MIDDLEWARE`
- Create a `CORS_ALLOWED_ORIGIN` at the bottom of the file (`settings.py`)
```python
INSTALLED_APPS = [
    ...
    # 3rd party
    'rest_framework',
    'corsheaders',

    # local apps
    'todos.apps.TodosConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # new
    'django.middleware.common.CommonMiddleware',
    ...
]

...

CORS_ALLOWED_ORIGIN = (
    'http://localhost:3000',
    'http://localhost:8000',
)
```
The former is the React App and the latter is the Django Server

