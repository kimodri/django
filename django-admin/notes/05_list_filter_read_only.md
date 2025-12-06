# 1. **Customizing List Display (`list_display`)**

`list_display` defines which columns appear in the **change list view** of the admin.

Example:

```python
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created_at')
```

### Key points:

* You can use **field names** from the model.
* You can also use **methods** or **properties** (with or without `@admin.display`) to show computed or custom values.
* Admin calls these methods for each row automatically.

Example with a method:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status_label')

    @admin.display(description="Status")
    def status_label(self, obj):
        return obj.get_status_display()  # Human-readable status
```

---

# 2. **Adding Filters (`list_filter`)**

`list_filter` creates a sidebar for filtering the displayed objects.

Example:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = ('status', 'category')
```

### Key points:

* Works with model **fields**, especially `BooleanField`, `ChoiceField`, `DateField`, `ForeignKey`, etc.
* Admin automatically generates filter options. For example:

  * `status` → choices displayed
  * `category` → related objects displayed
* Can also use **custom filters** for more advanced logic, but basic usage is just field names.

Example with a date filter:

```python
list_filter = ('status', 'category', 'created_at')  # created_at gets a date hierarchy filter
```

---

# 3. **Making Fields Read-Only (`readonly_fields`)**

`readonly_fields` prevents editing certain fields in the admin form.

Example:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'created_at')
```

### Key points:

* Fields listed in `readonly_fields` appear on the form but cannot be edited.
* You can include **methods or properties** in `readonly_fields` to display computed values.
* Example with a method:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('status_label',)

    @admin.display(description="Status")
    def status_label(self, obj):
        return obj.get_status_display()
```

---

# Summary Table

| Feature           | Purpose                            | How it works                                                                               |
| ----------------- | ---------------------------------- | ------------------------------------------------------------------------------------------ |
| `list_display`    | Customize columns in the list view | Accepts model fields, methods, or properties. Admin calls methods automatically.           |
| `list_filter`     | Add sidebar filters                | Accepts model fields. Admin generates filter options automatically.                        |
| `readonly_fields` | Make fields non-editable           | Fields are displayed but cannot be changed in the form. Can include methods or properties. |

---

# Example — Combined

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status_label', 'created_at_formatted')
    list_filter = ('status', 'category')
    readonly_fields = ('slug', 'status_label')

    @admin.display(description="Status")
    def status_label(self, obj):
        return obj.get_status_display()

    @admin.display(description="Created At")
    def created_at_formatted(self, obj):
        return obj.created_at.strftime("%b %d, %Y")
```

**Explanation:**

* `list_display` shows normal fields and custom methods.
* `list_filter` adds sidebar filters for `status` and `category`.
* `readonly_fields` prevents editing `slug` and displays the computed `status_label`.
