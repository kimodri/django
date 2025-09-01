# Deployment
- adding env variables
- switching to a PostgreSQL
- running thorugh Django's own deployment checklist

## Environment Variables
1. Install `environs[django]`: `pip install environs[django]`
2. Configure the `django_project/settings.py`
```python
# django_projects/settings.py
from pathlib import Path
from environs import Env

env = Env()
env.read_env()
```
3. Create a new hidden file called `.env` in the root project directory
4. add `.env` to our existing `.gitignore`
```git
.venv/
.env
__pycache__
db.sqlite3
```

## DEBUG & SECRET_KEY

### DEBUG
If you look at the `DEBUG` configuration in `django_project/settings.py` it is set to `True` 
- We want `DEBUG` to be true for local development yet `False` for production
- If there is difficulty loading the environemtn variables, we want to `DEBUG = False` so we're extra secure

1. Add `DEBUG=True` to the `.env` file
2. In `dj_project/settings.py` change the `DEBUG` to read the `DEBUG` variable from `.env` but with a default value to `False`
```python
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)
```
### SECRET_KEY
If you look at the current `django_project/settings.py`, the value is currently `django_insecure`
1. Generate a new `SECRET_KEY` cause you have committed it already
```shell
python -c 'import secrets;
print(secrets.token_urlsafe())'
```
on the command line
2. Copy paste the value to the `.env`

`SECRET_KEY=key`
3. Pass the `SECRET_KEY` variable by reading from `.env`
```python
SECRET_KEY=env.str("SECRET_KEY")
```
4. To confirm run the server

## ALLOWED HOSTS
In `dj_proj/settings.py` we will add three hosts here:
- `.herokuapp.com`
- `localhost`
- `127.0.0.1`
```python
ALLOWED_HOSTS = [".herokuapp.com", "localhost", "127.0.0.1"]
```

## DATABASES
The current database is SQLite but we want to be able to switch to PostgreSQL for production

When we installed `environs[django]` we also got the `dj-database-url` package
- This takes all the database configurations needed for our database (SQLite or Postgre) and creates a `DATABASE_URL` environment variable

1. Update the `DATABASES` configuration with `dj_db_url` from `environs` to help parse `DATABASE_URL`
```python
DATABASES = {
    'default': env.dj_db_url("DATABASE_URL")
}
```
2. Specify SQL as the local `DATABASE_URL` value in the `.env` file
```code
DEBUG=True
SECRET_KEY=Q0UrSq6QehlDP6RkPEJZC8HMoXLQuS6Qlc_q3nPj5KM
DATABASE_URL=sqlite:///db.sqlite3
```
- it is sqlite here because that is what we use but heroku will create another one

## Static Files 
This needs to be configured for browsable api to work
1. create a project level dir called `static`
2. Create an empty `.keep` file within the `static` directory so it is picked up by Git.
3. Install `whitenoise` to handle static files in production
4. WhiteNoise must be added to `django_project/settings.py` in the following locations
- `whitenoise` above `django.contrib.staticfiles` in `INSTALLED_APPS`
- `WhiteNoiseMiddleware` above `CommonMiddleware`
- `STATICFILES_STORAGE` configuration pointing to WhiteNoise
```python
# dj_project/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostalgic',  # new
    'django.contrib.staticfiles',
    'django.contrib.sites',  
    ...
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # new
    'corsheaders.middleware.CorsMiddleware',  
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR/"static"]  # new
STATIC_ROOT = BASE_DIR / "staticfiles"  # new
STATICFILES_STORAGE =  "whitenoise.storage.CompressedManifestStaticFilesStorage"  # new
```
5. run `collectstatic` so that all static directories and files are compiled into one location for deployment: `python manage.py collectstatic`

## Pyscopg and Gunicorn
1. [Psycopg](https://www.psycopg.org/docs/) a database adapter taht lets Python apps talk to PostgreSQL databases
    - if on mac install Homebrew and then `psycopg2`
    ```shell
    python -m pip install psycopg2
    ```
    - We can do this because Django's ORM translates our models.py code from python into the database backend of choice
    - Recommended to install `PostgreSQL` locally too
2. Gunicorn must be installed to to replace current Django web server which is only suitable for local deployment
`python -m pip install gunicorn`

### requirements.txt
`python -m pip freeze > requirements.txt`

