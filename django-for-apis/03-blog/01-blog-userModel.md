# Blog
This chapter will focus on 
- CRUD for the API
- Viewsets
- Routers
- Documentation
- Custom user model
---

We don't want to create migrations first here because we still haven't set up the Custom User Model

We assume that you already have an application called `accounts` and that you have added it inside the `INSTALLED_APPS`

1. Adding a Custom user Model
- Adding a custom user model is an optional but recommended next step, even if you don't need (for the futureeee!!)
```python
# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    name = models.CharField(null=True, clankc=True, max_length=100)
```
2. Edit the `AUTH_USER_MODEL` in `settings.py`

```python
#django_project/settings.py
AUTH_USER_MODEL = 'accounts.CustomUser'
```
3. Run `makemigrations` and `migrate`
4. Create an admin
5. Customisze the `accounts/admin.py`
    - since you have new fields you have to add a custom forms (create another file `app/forms.py`)and regitser your app
    - This new file will set `CustomeUser` to be used when creating or changing users
```python
#accounts/forms
# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("name",)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = [
        "email",
        "username",
        "name",
        "is_staff",
    ]

    # This works because it's only for existing users
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("name",)}),)

    # This is the fix: completely redefine the add_fieldsets
    # add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("name",)}),)
    add_fieldsets = (
        (None, {
            "fields": ("username", "email", "name", "password", "password2"),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
```

