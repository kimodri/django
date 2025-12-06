# Setting up Custom Admin

- Setting up custom admin site
- Overriding the default admin site
- Setup multiple admin areas

### 1\. Setting up a Custom Admin Site

If you want to create a specific admin interface with its own branding and specific set of models (separate from the global default), you should subclass `AdminSite`.

**Step 1: Create the Custom Admin Class**
In your app (e.g., `core/admin.py` or a new file `core/sites.py`), define your custom site class.

```python
# core/sites.py
from django.contrib.admin import AdminSite

class ClientAdminSite(AdminSite):
    site_header = "Client Portal"
    site_title = "Client Admin Portal"
    index_title = "Welcome to the Client Portal"

# Create an instance of the site
client_admin_site = ClientAdminSite(name='client_admin')
```

**Step 2: Register Models to this Specific Site**
Unlike the default admin where you use `@admin.register`, you must register models explicitly to your new instance.

```python
# core/admin.py
from .models import Order, Invoice
from .sites import client_admin_site

# Register models only to the custom site
client_admin_site.register(Order)
client_admin_site.register(Invoice)
```

**Step 3: Add to URL Configuration**
Hook the custom site into your `urls.py`.

```python
# project/urls.py
from django.urls import path
from core.sites import client_admin_site

urlpatterns = [
    # Access this at /client-portal/
    path('client-portal/', client_admin_site.urls),
]
```

-----

### 2\. Overriding the Default Admin Site

There are two ways to do this. The **Simple Way** (changing titles) and the **Advanced Way** (replacing the underlying class logic).

#### Method A: The Simple Way (Configuration)

If you just want to change the text "Django Administration" to your project name, you don't need a custom class. Just add this to your main `urls.py`:

```python
# project/urls.py
from django.contrib import admin
from django.urls import path

# Override properties of the default instance
admin.site.site_header = "My Project Administration"
admin.site.site_title = "My Project Admin"
admin.site.index_title = "Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
]
```

#### Method B: The Advanced Way (Class Replacement)

If you need to change the *logic* of the default admin (e.g., how it checks permissions or loads templates globally), you should replace the default class entirely using `AppConfig`.

1.  **Create your custom class** (as shown in Guide \#1).
2.  **Create a custom AppConfig** in `core/apps.py`:

<!-- end list -->

```python
# core/apps.py
from django.contrib.admin.apps import AdminConfig

class MyCustomAdminConfig(AdminConfig):
    default_site = 'core.sites.MyCustomAdminSite' # Path to your custom class
```

3.  **Update `INSTALLED_APPS`** in `settings.py`. You must remove `django.contrib.admin` and replace it with your custom config:

<!-- end list -->

```python
# settings.py
INSTALLED_APPS = [
    # 'django.contrib.admin',  <-- Remove this
    'core.apps.MyCustomAdminConfig', # <-- Add this
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # ...
]
```

-----

### 3\. Setup Multiple Admin Areas

A common use case is having a Superuser Admin (for developers) and a Restricted Admin (for store managers or HR). You can run both simultaneously.

**Scenario:**

  * `/admin/` = Full access (Default Django Admin).
  * `/hr-admin/` = Restricted access (Only Employee and Department models).

**Step 1: Keep the Default Admin**
Keep `django.contrib.admin` in your `INSTALLED_APPS` and keep the default registration in `urls.py`.

**Step 2: Create the Second Admin Instance**
Create a new file `hr/admin.py` (or wherever your HR app is).

```python
# hr/admin.py
from django.contrib.admin import AdminSite
from .models import Employee, Department

class HRAdminSite(AdminSite):
    site_header = "HR Management"
    site_title = "HR Portal"

# Instantiate it
hr_admin_site = HRAdminSite(name='hr_admin')

# Register models ONLY to this specific instance
hr_admin_site.register(Employee)
hr_admin_site.register(Department)
```

**Step 3: Define URLs for Both**
In your main `urls.py`, route them to different paths.

```python
# project/urls.py
from django.contrib import admin # The default one
from django.urls import path
from hr.admin import hr_admin_site # The custom one

urlpatterns = [
    # The default full admin
    path('admin/', admin.site.urls),
    
    # The restricted HR admin
    path('hr-admin/', hr_admin_site.urls),
]
```

**Step 4: Permissions (Optional but Recommended)**
By default, `AdminSite` checks if `user.is_staff == True`. If you want the HR admin to be accessible by users who are *not* global staff, you can override the `has_permission` method in your custom class:

```python
class HRAdminSite(AdminSite):
    def has_permission(self, request):
        # Allow access if user is active and belongs to the HR group
        return request.user.is_active and request.user.groups.filter(name='HR').exists()
```

-----

### Summary of Differences

| Feature | Default Admin (`admin.site`) | Custom Admin (`MySite`) |
| :--- | :--- | :--- |
| **Setup** | Built-in, enabled in settings. | Must create a class inheriting `AdminSite`. |
| **Registration** | `@admin.register(Model)` | `my_site.register(Model)` |
| **Use Case** | Global system management. | Specific stakeholder dashboards (HR, Vendors). |
