# 1. What a Django form is

A Django form is a Python class that:

* Defines fields
* Renders HTML
* Validates user input
* Returns cleaned data

Two families exist:

### a. `forms.Form`

Pure form, not tied to a model.

```python
# app/forms.py
from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField()
    message = forms.CharField()
```

### b. `forms.ModelForm`

A form automatically built from a model.

```python
# app/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
```

This is the most common form type in Django admin and CRUD views.

---

# 2. Why customize forms?

Three basic reasons:

### Reason 1: Control what the user sees

You can change field order, labels, widgets, placeholders, etc.

### Reason 2: Control how input is validated

You can add your own validation rules beyond what the model enforces.

### Reason 3: Control what happens when the form saves

You can add attributes that are not directly provided by the user.

These three ideas are the foundation of form customization.

---

# 3. The three core places you customize a form

You only need to remember these three:

### (1) Field definitions

Either override fields or define new ones.

```python
class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=50, label="Post Title")
```

### (2) Validation methods

Two main techniques:

```python
def clean_title(self):
    title = self.cleaned_data["title"]
    if "?" in title:
        raise forms.ValidationError("No question marks allowed.")
    return title
```

```python
def clean(self):
    data = super().clean()
    # cross-field validation
    return data
```

### (3) The `__init__` method or Meta widgets

The `__init__` lets you change behavior or widgets dynamically.

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['title'].widget.attrs['placeholder'] = 'Enter title'
```

---

# 4. How forms are connected to the admin

The Django admin uses your `ModelForm` automatically unless you override it.

Basic example:

```python
# app/admin.py
from django.contrib import admin
from .models import Post
from .forms import PostForm

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
```

This means:

* When you open the admin "add post" page
* Django instantiates your form
* Your custom validation and widgets apply

The admin simply acts as a specialized view that calls:

```
form = PostForm(request.POST or None)
form.is_valid()
form.save()
```

Exactly how your own view would.

---

# 5. The full lifecycle (from request to DB save)

This is the simplest way to visualize how form customization works.

1. User opens a page
2. Django instantiates a form

```python
form = PostForm()
```

3. User submits POST
4. Django re-instantiates with submitted data

```python
form = PostForm(request.POST)
```

5. `form.is_valid()` triggers:

   * `clean_<field>()`
   * `clean()`
   * model validation if ModelForm

6. If valid:

```python
form.save()
```

7. Form creates/updates a model instance

Everything you customize affects steps 3–7.

---

# 6. Basic example: customize widget, validation, and save

```python
# app/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title'})
        }

    def clean_title(self):
        t = self.cleaned_data['title']
        if len(t) < 3:
            raise forms.ValidationError("Title too short.")
        return t

    def save(self, commit=True):
        post = super().save(commit=False)
        post.slug = post.title.lower().replace(" ", "-")
        if commit:
            post.save()
        return post
```

This represents the three basic customizations:

* Presentation
* Validation
* Save behavior

---

# 7. Basic admin integration

```python
# app/admin.py
from django.contrib import admin
from .models import Post
from .forms import PostForm

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
```

Now your admin “Add Post” and “Edit Post” pages use your custom behavior.

---

# 8. Summary: what you should understand at this level

You now know:

* The difference between `Form` and `ModelForm`
* Why you customize forms
* The three main customization points: fields, validation, save
* How the admin uses your forms
* The full lifecycle of a form submission

This is the foundation that everything else builds on (widgets, formsets, dynamic behavior, inline admin, etc.).
