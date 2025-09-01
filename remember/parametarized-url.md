### Path Converters (`<int:pk>`) 

In Django's `path()` function, `<int:pk>` is called a **path converter**. It's a powerful tool that tells Django to do two things at once:

1.  **Capture a parameter**: The part `<int:pk>` tells Django to capture whatever value is in that position in the URL.
2.  **Convert its type**: The `int:` part is a type converter. It ensures that the captured value is a valid integer. If you try to visit `/todo/hello/`, Django will throw an error because "hello" can't be converted to an integer.

The captured value is then passed as a keyword argument to the view function or class (`DetailTodo.as_view()` in your example). So, if the URL is `/todo/5/`, the `DetailTodo` view will receive the argument `pk=5`.

### "How Does It Know It's a Primary Key?" 

Django **doesn't** automatically know that `pk` stands for "primary key." That's a developer convention. `pk` is widely used because it's a short, clear way to refer to the primary key, which is the most common parameter for retrieving a single object.

You could use any name you like, as long as it's a valid Python variable name. For example:

```python
path("<int:todo_id>/", DetailTodo.as_view(), name="todo_detail"),
```

In this case, the captured value would be passed to the view as `todo_id=5`. Your view would need to be written to accept `todo_id` instead of `pk`.

### The URL Pattern in Action

Let's look at your `urlpatterns` with this understanding:

  * `path("", ListTodo.as_view(), ...)`: This URL pattern matches an empty string, meaning the base URL (e.g., `www.yoursite.com/api/todos/`). It doesn't have any parameters and will call the `ListTodo` view, which retrieves all the to-do items.
  * `path("<int:pk>/", DetailTodo.as_view(), ...)`: This pattern matches a URL with an integer at the end (e.g., `www.yoursite.com/api/todos/5/`). It captures the `5`, and passes it to the `DetailTodo` view. The `DetailTodo` view then uses this `pk` value to look up the single to-do item with that primary key.

In short, parametrized URLs give you a flexible way to build dynamic, data-driven endpoints for your API.