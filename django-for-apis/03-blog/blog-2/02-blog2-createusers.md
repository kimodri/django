# Create a user
Just create a user in the admin

# Login
Now that you have a user, how can they have an access to the api specifically the api results? To do that:
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('posts.urls')),
    path("api-auth/", include('rest_framework.urls'))  # new
]
```
Now at the top of the browsable API, it will have a log/logout