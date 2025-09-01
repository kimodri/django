You are correct. It is a best practice to create a custom user model from the start of a Django project. Here is a guide in markdown format with sample code.

# Why Use a Custom User Model?

Even if you don't need to add any fields to your user model right away, creating a custom one is essential for **future-proofing** your project. Once you have database tables and relationships tied to Django's default user model, changing it becomes a difficult and tedious process. A custom model gives you the flexibility to easily add or modify user-related fields later on, such as a phone number, a profile picture, or an API key.

-----

## Step 1: Create a Custom App for the User Model

It is a good practice to keep your user model separate from your main project or other apps.

```bash
python manage.py startapp accounts
```

Add the new `accounts` app to your `INSTALLED_APPS` in `settings.py`.

```python
# settings.py

INSTALLED_APPS = [
    # ... other apps
    "accounts",
]
```

-----

## Step 2: Define the Custom User Model

There are two main ways to define a custom user model. For most cases, **`AbstractUser`** is the recommended choice as it provides a lot of functionality out-of-the-box, allowing you to focus on adding your own fields.

### Option 1: Using `AbstractUser` (Recommended) ✅

This approach is best if you want to keep Django's built-in fields like `first_name`, `last_name`, and `is_staff`, but want to use the user's **email as the primary login field** instead of a username.

**`accounts/models.py`**

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Overwrite the default username field with None
    username = None

    # Set email as a unique, required field
    email = models.EmailField(unique=True, null=False, blank=False)
    
    # You can add new custom fields here!
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Tell Django to use the 'email' field for authentication
    USERNAME_FIELD = 'email'
    
    # Required fields for creating a user via `createsuperuser`
    REQUIRED_FIELDS = []
```

### Option 2: Using `AbstractBaseUser`

This is for when you need to completely customize your user model from the ground up and require more control over the authentication process. It requires more boilerplate code, including a custom manager.

**`accounts/models.py`**

```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
        
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser
```

-----

## Step 3: Tell Django to Use Your Custom Model

You must configure Django to use your new custom user model instead of the default one. **This must be done before you run your first migrations.**

Add the following line to your `settings.py` file:

```python
# settings.py

AUTH_USER_MODEL = 'accounts.CustomUser'
```

-----

## Step 4: Create and Apply Migrations

Now you can create your database schema based on your new user model.

```bash
python manage.py makemigrations accounts
python manage.py migrate
```

After these steps, your Django project will use your custom user model, and you can add new fields and functionalities to it whenever you need to in the future.