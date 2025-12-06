### 1\. Selecting Fields (Limiting Input)

By default, the Admin displays every editable field in your model. Sometimes you want to hide fields (like internal timestamps) or reorder them.

You use the `fields` attribute to whitelist exactly what should appear and in what order.

**Example:** Let's configure the **Publisher** admin to only show the name and website, hiding the email.

```python
# bookstore/admin.py
from django.contrib import admin
from .models import Publisher, Book

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    # Only these fields will appear in the form
    fields = ['name', 'website']
    
    # Alternatively, you can use 'exclude' to hide specific fields 
    # and show everything else:
    # exclude = ['email']
```

-----

### 2\. Fieldsets (Grouping, Descriptions, Classes)

When you have a large model like **Book** (which has prices, stock, authors, dates, etc.), a long list of input boxes looks messy.

**Fieldsets** allow you to group fields into sections.

  * **Structure:** A list of tuples. `(Section Name, {Options Dictionary})`.
  * **Classes:** CSS classes to style the section. `'collapse'` makes the section accordioned (hidden by default).
  * **Description:** Adds instructions at the top of the section.

<!-- end list -->

```python
# bookstore/admin.py

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fieldsets = (
        # Section 1: Standard Info (No header name, hence None)
        (None, {
            'fields': ('title', 'publisher', 'authors')
        }),
        
        # Section 2: Inventory Management
        ('Inventory', {
            'fields': ('stock_count', 'price', 'isbn'),
            # 'classes': ('wide',) is standard Django CSS for extra width
            'description': "Manage the physical attributes of the book here."
        }),
        
        # Section 3: Publishing Details (Collapsible)
        ('Meta Data', {
            'fields': ('publication_date',),
            # 'collapse' makes this section hidden until clicked
            'classes': ('collapse',), 
        }),
    )
    
    # Bonus: Use this for ManyToMany fields (like authors) 
    # to make selecting easier than a multi-select box
    filter_horizontal = ('authors',)
```

-----

### 3\. Help Text

There are two places to define the helpful "grey text" that appears under an input field.

**A. In the Model (Global)**
This is the preferred way. You already did this in your `Book` model:

```python
# bookstore/models.py
isbn = models.CharField(..., help_text="13 Character ISBN number")
```

**B. In the Admin Form (Context Specific)**
If you want help text *only* for the admin panel (and not for the front-end users), you can inject it using `help_texts` inside a custom form (see Section 4 below).

-----

### 4\. Building a Custom Form

Sometimes the default configuration isn't enough. You might want to:

1.  Add custom **validation logic** (e.g., "Title cannot be all UPPERCASE").
2.  Change a widget (e.g., use a smaller text area).
3.  Add specific help text just for admins.

To do this, you create a `ModelForm`, and then tell the `ModelAdmin` to use it.

**Step 1: Create the Form**
Create a new file `blog/forms.py`.

```python
# blog/forms.py
from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostAdminForm(forms.ModelForm):
    # 1. Customizing a widget or help text without changing the Model
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'special-css-class'}),
        help_text="Please enter a catchy title (Admin only note)."
    )

    class Meta:
        model = Post
        fields = '__all__'

    # 2. Custom Validation Logic
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title.isupper():
            raise ValidationError("Please do not use ALL CAPS in the title.")
        return title
```

**Step 2: Connect Form to Admin**
Update your `blog/admin.py` to use this form.

```python
# blog/admin.py
from django.contrib import admin
from .models import Post
from .forms import PostAdminForm # Import your custom form

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Tell Django to use your custom form class
    form = PostAdminForm
    
    list_display = ('title', 'category', 'options')
    # ... rest of your config
```