# Simple Customization
You can customize simple things in the admin inside the `project/urls.py`

```python
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

"""
Here you can add your simple django admin customization:
1. index title
2. site header
3. site title
"""
admin.site.index_title = "The Bookstore"
admin.site.site_header = "The Bookstore"
admin.site.site_title = "Bookstore"
```