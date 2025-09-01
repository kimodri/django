# CORS For Blog
Since the app is most likely be consumed by another port (domain)

1. Install the `django-cors-headers`
2. Add `corsheaders` to `INSTALLED_APPS`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'rest_framework',
    'corsheaders',  # new

    # local apps
    'accounts.apps.AccountsConfig',
    'posts.apps.PostsConfig',
]
```
3. Add `CorsMiddleware` to the `MIDDLEWARE` setting
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # new
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
``` 
4. Create a `CORS_ALLOWED_ORIGINS`  
```python
CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "http://localhost:8000",
)
```
# CSRF
In the event that our API will be used in forms we should also configure `CSRF_TRUSTED_ORIGINS` 
```python
# django_project/setting.py
CSRF_TRUSTED_ORIGINS = ["https://localhost:3000"]
```