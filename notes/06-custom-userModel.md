# Custom User Model

To create a custom user model for a Django backend that serves a React frontend, you'll extend Django's built-in `AbstractUser` class. This allows you to add custom fields to the user profile while keeping Django's core authentication functionality, which you'll expose through an API.
- It is important to not run `makemigrations` and migrate to this

## Creating a Custom User Model
Creating one requires four steps:
1. update `django_project/settings.py`
2. create a new `CustomUser` model
3. create a new forms for `UserCreationForm` and `UserChangeForm`
4. update `accounts/admin.py` 
-----
### Step 1: Update `settings.py`

You must explicitly tell Django to use your new `CustomUser` model instead of its default `User` model. Add the following line to your `settings.py` file.

```python
# your_project_name/settings.py

AUTH_USER_MODEL = 'your_app_name.CustomUser'
```

### Step 2: Create the Custom User Model

In your Django app's `models.py` file, define a new model that inherits from `AbstractUser`. This is where you'll add any fields specific to your application's users.

```python
# your_app_name/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null = True, blank = True)
```
-  In practice, `null` and `blank` are commonly used together in this fashion so that a form allows an empty value and the database stores that value as NULL.

### Step 3: Forms
What are the two ways in which we would interact with out new `CustomUser` model? 
- When a user signs up (creation)
- When an admin edits (edition)

We will need to update two built-in forms for this functionality: `UserCreationForm` and `UserChangeForm`

- Create a new file called `accounts/forms.py` and update it with the following code:
```python
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(AdminUserCreationForm):
    class Meta(AdminUserCreationForm):
        model = CustomUser
        fields = AdminUserCreationForm.Meta.fields + ("age",)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
```
- We use `Meta Class` to override the default fields by setting the `model` to our `CustomUser` and using the default fields via `Meta.fields` which includes all default fields
- To add the custom fields, `age`, we simply tack it on at the end

#### Fields in custom User Model 
-  Our CustomUsermodel containsall the fields of the default Usermodel ando uradditional age field which we set. But what are these default fields? It turns out there are many including `username`, `first_name`,`last_name`, `email`, `password`, `groups`, and more. 
- Yet when a user signs up for a new account on Django the default form only asks for a `username`, `email`, and `password`. This tells us that the default setting for `fields` on `UserCreationForm` is just username, email, and password eventhough there are many more fields available.

### Step 4: `<app>/admin.py`
If there's a problem in here, look at the implementation of the blog app in `accounts/admin.py`

We need to update the admin so these changes will show on the page.
- We will extend the existing `UserAdmin` class to use our new `CustomUser` model 
    - `UserAdmin` is the user model that is coupled with the admin so we need to ovveride some of it
    - `list_display`: to control which fields are listed
    - `fieldsets`: edit and add new custom fields like age (for fields use in editing users)
    - `add_fieldsets`: to add (for fiels used when creating a user)
```python
# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
            "email",
            "username",
            "age",
            "is_staff",
        ]

    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("age",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("age",)}),)
    admin.site.register(CustomUser, CustomUserAdmin)
```
### Step 5: Create and Apply Migrations

After defining the model and updating your settings, you need to create and apply a database migration to create the new table for your custom user model.

```bash
python manage.py makemigrations your_app_name
python manage.py migrate
```

-----

### How This Works with Your React Frontend

Your React frontend will continue to use API calls to interact with this custom user model. You'll still use Django REST Framework (DRF) to handle authentication and data serialization.

  * **Authentication**: When a user logs in via an API endpoint, DRF's authentication classes will now look up and verify the user against your `CustomUser` model.
  * **Data Access**: When your React app makes an authenticated request, you can access the custom fields (like `bio` or `is_premium_member`) from the `request.user` object in your Django views. You can then include these custom fields in the JSON response that is sent back to the React app.

-----

