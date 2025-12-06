# 1. What is a custom model method?

A **custom model method** is simply a Python method you define inside a Django model class.
It expresses something the model *can do* or *compute*.

Example:

```python
class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(null=True, blank=True)

    def publish(self):
        """Business logic: mark this article as published."""
        from django.utils import timezone
        self.published_at = timezone.now()
        self.save(update_fields=['published_at'])
```

The method belongs to the model, not the view.

---

# 2. Why the method is inside the model (not the view)

### A. Models = business logic

Models should contain logic **about the data itself**
Views should only handle the request/response cycle.

**Model method:**

* “What does an Article do?” → It can `publish()`
* “How do you compute something about an Article?” → e.g., `word_count`

**View:**

* Receives HTTP request
* Fetches a model object
* Calls model methods
* Returns a response

### B. View = thin

View should not contain business rules.

Instead of:

```python
def publish_article(request, pk):
    article = Article.objects.get(pk=pk)
    article.published_at = timezone.now()
    article.save()
```

Do this:

```python
def publish_article(request, pk):
    article = Article.objects.get(pk=pk)
    article.publish()              # ← calling the model method
    return redirect("articles:list")
```

### Why this is better:

* You reuse the same logic in admin, APIs, shell, background tasks, signals.
* View is smaller and easier to read.
* All business rules live in one place.

This is the **separation of concerns**:

* View handles HTTP.
* Model handles business logic.

---

# 3. When do we call model methods in the views?

Answer: **Whenever your view needs the model to perform its own behavior.**

Examples:

### A. Editing data

```python
article.publish()
```

### B. Calculating something

```python
price = cart.calculate_total()
```

### C. Performing an action

```python
order.cancel()
user.send_activation_email()
profile.generate_avatar()
```

### D. Getting derived data (properties)

```python
if article.is_published:
    ...
```

### E. Preparing data

```python
invoice = order.generate_invoice()
```

### F. Cleaning logic

```python
username = user.create_unique_username()
```

**Rule:**
If it belongs to the model’s behavior → call the model method from the view.

---

# 4. How admin interacts with custom model methods

When you register a model in admin:

```python
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'word_count')
```

Admin automatically calls:

```python
obj.is_published
obj.word_count
```

for each row displayed.

You may also call methods manually in admin actions:

```python
@admin.action(description="Publish selected articles")
def publish_selected(modeladmin, request, queryset):
    for article in queryset:
        article.publish()        # ← calling the model method
```

Admin also uses methods in:

* read-only fields
* list filters
* list displays
* custom buttons (Django 4.1+)
* form clean or save logic

**Key idea:**
Admin interacts with your model exactly like your view does—by calling methods on the model.

---

# 5. Why admin benefits from model methods

If business logic is in the model, both your admin and your API can do this:

```python
article.publish()
```

Instead of duplicating the logic inside the admin class and inside the view.

Again: **models = behavior**, **views/admin = consumers of that behavior**.

---

# 6. Summary of the separation

### Models:

* Represent the data + the rules that govern that data
* Have methods that express business logic
* Are reusable in shell, admin, scripts, API, celery tasks, tests, views

### Views:

* Receive request
* Get models
* Call model methods
* Return response

### Admin:

* Calls model methods to show data
* Calls model methods in actions
* Respects properties and methods automatically

