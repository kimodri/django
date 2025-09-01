# Class-Based Views
Apparently this is better that function views LOLs

There are lots of `views` classes that we can extend upn such as:
- TemplateView
- ListView

So for example, if you just want to view a template, you can do:
```python
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = "home.html"
```

Now since you changed your view, you would also need to change the `urls.py` in project and app level
```python
# django_project/urls.py
from django.contrib import admin
from django.urls import path, include # new

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")), # new
 ]
```
In the app level:
```python
# pages/urls.py
from django.urls import path
from .views import HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    ]
```
- You only add `as_view()` at the end of the view name

## Other Classes
...