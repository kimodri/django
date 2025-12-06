### 1\. Customizing Models with Decorators

**Why do this?**
By default, Django only shows the "string representation" (the `__str__` method) of your object in the admin list. This is often insufficient for managing data.

To gain fine-grained control—such as adding columns, sidebar filters, search bars, and grouping fields on the edit page—you must use the `ModelAdmin` class. The cleanest and most modern way to apply this is using the `@admin.register` decorator.

Here is a comprehensive example for your **Blog** app.

```python
# blog/admin.py
from django.contrib import admin
from .models import Post, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 1. LIST DISPLAY: The Columns
    # Instead of just seeing "Post object (1)", we define exactly which 
    # fields appear as columns in the table.
    list_display = ('title', 'category', 'status_label', 'created_at_formatted')

    # 2. LIST FILTER: The Sidebar
    # This adds a box on the right side of the screen allowing admins to 
    # filter results by specific fields (e.g., show only 'published' posts).
    list_filter = ('options', 'category')

    # 3. SEARCH FIELDS: The Search Box
    # This enables the search bar at the top. You can use double underscores 
    # to search inside related models (e.g., searching the Category name).
    search_fields = ('title', 'category__name')

    # 4. FIELDSETS: The Edit Layout
    # By default, Django stacks all fields vertically. Fieldsets allow you 
    # to group related fields into sections (e.g., "Main Content" vs "Meta Data").
    fieldsets = (
        ('Main Content', {
            'fields': ('title', 'category', 'options')
        }),
        ('Advanced Options', {
            'classes': ('collapse',), # This makes the section clickable/collapsible
            'fields': ('slug',), 
        }),
    )

    # 5. PREPOPULATED FIELDS
    # This is magic for blogs. As you type the 'title', Django will 
    # automatically fill the 'slug' field for you.
    prepopulated_fields = {'slug': ('title',)}

    # CUSTOM METHODS (Calculated Columns)
    # Sometimes you want to display data that isn't a direct field in the database.
    
    @admin.display(description="Status")
    def status_label(self, obj):
        # Displays the human-readable version (e.g., "Published" instead of "published")
        return obj.get_options_display()

    @admin.display(description="Created At", ordering='id')
    def created_at_formatted(self, obj):
        # Example of formatting a date, assuming you add a created_at field later
        # We assume 'id' roughly correlates to creation time for sorting
        return "Recent" if obj.id > 10 else "Archived"


# For simple models like Category, we can keep it minimal
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
```

-----

### 2\. Looping Through All Models (Bulk Registration)

**Why do this?**
In large applications (like a `bookstore` with `Book`, `Author`, `Publisher`, `Inventory`, `Review`, `Tag`), manually writing an `admin.register` block for every single model is tedious and error-prone. If you forget one, it simply won't appear in the admin.

The "Loop Strategy" ensures that **every** model in your app is registered automatically. If you haven't defined a custom view for it, this script will generate a basic one for you.

Here is how to implement this for your **Bookstore** app.

```python
# bookstore/admin.py
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

# 1. GET APP CONFIGURATION
# We need to tell Django exactly which app we are looking at. 
# Make sure 'bookstore' matches the name in your INSTALLED_APPS.
app_config = apps.get_app_config('bookstore')

# 2. FETCH MODELS
# This retrieves a list of every model class defined in bookstore/models.py
models = app_config.get_models()

# 3. THE LOOP
for model in models:
    try:
        # 4. DYNAMIC ADMIN CLASS
        # Instead of just registering the model (which only shows the __str__),
        # we create a temporary Admin class on the fly.
        
        class DynamicAdmin(admin.ModelAdmin):
            # This list comprehension gets all field names from the model
            # so they all appear as columns in the admin list.
            list_display = [field.name for field in model._meta.fields]
            
            # Optional: Add search for any text fields automatically
            search_fields = [
                field.name for field in model._meta.fields 
                if field.get_internal_type() in ['CharField', 'TextField']
            ]

        # Register the model with our dynamically created class
        admin.site.register(model, DynamicAdmin)
        
    except AlreadyRegistered:
        # This is the safety net. If you already manually registered a complex 
        # model (like a 'Book' model with specific logic) using @admin.register above,
        # this error will trigger. We simply 'pass' to skip it and keep the 
        # custom version you wrote.
        pass
```