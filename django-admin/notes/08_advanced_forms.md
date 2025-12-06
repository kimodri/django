# 1. Quick orientation: `Form` vs `ModelForm`

* `forms.Form` — full control; no model coupling; useful for multi-step wizards, pure UI, or operations not directly mapped to one model.
* `forms.ModelForm` — tied to a model; generates fields automatically; use when mapping to DB rows and using `save()`.

Use `ModelForm` when you want automatic saving and validation based on model fields; use `Form` when not saving to a single model instance.

---

# 2. Validation patterns

### Where to put validation

* Field-level validators: `validators` on model/field or `validators` on form field. Good for reusable rules.
* Form `clean_<field>()`: validate/transform single field.
* Form `clean()`: cross-field validation and adding `non_field_errors`.
* Model `clean()` (and `full_clean()`): put model invariants there (useful if forms are not the only entry point).

### Example: `clean_<field>` and `clean()`

```python
# app/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import ExtractionConfig

class ExtractionConfigForm(forms.ModelForm):
    class Meta:
        model = ExtractionConfig
        fields = ['name', 'source', 'schedule']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if ' ' in name:
            raise ValidationError("no spaces allowed in name.")
        return name

    def clean(self):
        cleaned = super().clean()
        source = cleaned.get('source')
        schedule = cleaned.get('schedule')
        if source == 'db' and not schedule:
            raise ValidationError("DB sources require a schedule.")
        return cleaned
```

---

# 3. Custom validators (reusable)

```python
# app/validators.py
from django.core.exceptions import ValidationError

def validate_no_special_chars(value):
    if any(ch in value for ch in "!@#$%^&*()"):
        raise ValidationError("No special characters allowed.")
```

Apply in model or form:

```python
# app/models.py (field-level)
from django.db import models
from .validators import validate_no_special_chars

class ExtractionConfig(models.Model):
    name = models.CharField(max_length=200, validators=[validate_no_special_chars])
```

---

# 4. Widgets, attributes, and presentation

* Customize widget via `widgets` in `Meta` or by overriding field in the form.
* Use `attrs` to add classes, data-attributes, placeholder, `readonly`, etc.

```python
# app/forms.py
from django import forms
from .models import ExtractionConfig

class ExtractionConfigForm(forms.ModelForm):
    class Meta:
        model = ExtractionConfig
        fields = ['name', 'source', 'schedule']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'vTextField', 'placeholder': 'config-name'}),
            'schedule': forms.TextInput(attrs={'placeholder': 'cron or empty'}),
        }
```

For complex widgets, write a custom widget class.

---

# 5. `save()` patterns (ModelForm)

* `form.save(commit=False)` → set extra attributes, call `instance.save()`, then `form.save_m2m()`.
* Use `transaction.atomic()` when saving multiple related objects.

```python
# app/forms.py
from django.db import transaction

class ExtractionConfigForm(forms.ModelForm):
    def save(self, commit=True, triggered_by=None):
        instance = super().save(commit=False)
        if triggered_by:
            instance.modified_by = triggered_by
        if commit:
            with transaction.atomic():
                instance.save()
                self.save_m2m()
        return instance
```

---

# 6. Read-only / disabled fields in forms vs admin

* Form-level: set `field.disabled = True` or `widget.attrs['readonly'] = True` to prevent edits (disabled fields aren’t submitted).
* Admin: `readonly_fields` shows fields but keeps them uneditable in the admin form; this is different from `disabled` on a form field.

Example to render a computed field read-only:

```python
# app/forms.py
class ExtractionConfigForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].disabled = True  # shows but not editable
```

---

# 7. File uploads and large files

* For large uploads, prefer streaming/chunked uploads from the client and processing them in background workers.
* Django’s `request.FILES` gives `InMemoryUploadedFile` or `TemporaryUploadedFile` depending on size. Use `upload_handlers` or third-party uploaders for very large files.

Example handling file in view:

```python
# app/views.py
from django.shortcuts import render, redirect
from .forms import UploadForm

def upload_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = request.FILES['datafile']
            # Save and enqueue processing
            instance = form.save()
            # enqueue worker to process file instance.pk
            return redirect('success')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})
```

---

# 8. Formsets and inline formsets

* `formset_factory()` for multiple copies of a `Form`.
* `inlineformset_factory(parent_model, child_model, ...)` for editing related objects (one-to-many) in a single form.
* In admin, use `InlineModelAdmin` (TabularInline / StackedInline) for per-parent inlines.

Example inline formset in views:

```python
# app/forms.py
from django.forms import inlineformset_factory
from .models import ExtractionConfig, ExtractionParameter

ExtractionParameterFormSet = inlineformset_factory(
    ExtractionConfig, ExtractionParameter,
    fields=('key', 'value'), extra=1, can_delete=True
)
```

In admin use `class ExtractionParameterInline(admin.TabularInline)`.

---

# 9. Admin-specific form customization

* Supply `form = YourForm` in `ModelAdmin` to replace the default admin form.
* Use `formfield_overrides` to change widget for a model field across the admin.
* `get_form()` / `get_formset()` allow dynamic form behavior based on `request`.
* Use `autocomplete_fields`, `raw_id_fields`, `filter_horizontal` to improve performance for FK/M2M.

Example:

```python
# app/admin.py
from django.contrib import admin
from .models import ExtractionConfig
from .forms import ExtractionConfigForm

@admin.register(ExtractionConfig)
class ExtractionConfigAdmin(admin.ModelAdmin):
    form = ExtractionConfigForm
    list_display = ('name', 'source')
    readonly_fields = ('last_run',)
    autocomplete_fields = ('related_big_foreignkey',)
```

Dynamically set fields per user:

```python
def get_form(self, request, obj=None, **kwargs):
    form = super().get_form(request, obj, **kwargs)
    if not request.user.is_superuser:
        form.base_fields['source'].disabled = True
    return form
```

---

# 10. Inline admin formsets (custom validation)

* Override `BaseInlineFormSet.clean()` to validate relationships across inlines.

```python
# app/admin.py
from django.forms.models import BaseInlineFormSet

class ParamInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        keys = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            key = form.cleaned_data.get('key')
            if key in keys:
                raise ValidationError("Duplicate parameter keys.")
            keys.append(key)
```

---

# 11. Custom widgets & widget Media (JS/CSS)

* Create widgets with `Media` to include JS/CSS for admin or normal forms.

```python
# app/widgets.py
from django.forms import TextInput

class CronWidget(TextInput):
    class Media:
        js = ('js/cron-helper.js',)
        css = {'all': ('css/cron-helper.css',)}
```

Use in form:

```python
# app/forms.py
class ExtractionConfigForm(forms.ModelForm):
    class Meta:
        widgets = {'schedule': CronWidget()}
```

---

# 12. Autocomplete and performance

* For large FK/M2M sets, use `autocomplete_fields` in admin or AJAX-powered Select2 in custom forms.
* Use `select_related` / `prefetch_related` where necessary in views or admin `get_queryset()` to avoid N+1 queries.

---

# 13. Testing forms

* Unit test `Form.is_valid()`, field errors, `form.save(commit=False)` behavior.
* Use `Client` to post admin actions and assert that logs were created or messages returned.

Example unit test:

```python
# app/tests.py
from django.test import TestCase
from .forms import ExtractionConfigForm

class ExtractionFormTests(TestCase):
    def test_name_validation(self):
        form = ExtractionConfigForm({'name': 'bad name', 'source': 'api'})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
```

---

# 14. Security & best practices

* CSRF protection for all POST endpoints (Django admin already handles this).
* Use `clean()` and model-level validation to ensure invariants are enforced even if data is created outside forms.
* Avoid executing long-running work synchronously in `save()` or admin actions — always enqueue.
* Don’t trust client-side widget logic for validation; enforce server-side rules.

---

# 15. Example: cohesive mini-stack (models, forms, admin)

```python
# app/models.py
# (excerpt)
class ExtractionConfig(models.Model):
    name = models.CharField(max_length=200, unique=True)
    source = models.CharField(max_length=200)
    last_run = models.DateTimeField(null=True, blank=True)
```

```python
# app/forms.py
from django import forms
from .models import ExtractionConfig
from .validators import validate_no_special_chars

class ExtractionConfigForm(forms.ModelForm):
    class Meta:
        model = ExtractionConfig
        fields = ['name', 'source']
        widgets = {'name': forms.TextInput(attrs={'placeholder': 'config-name'})}

    name = forms.CharField(validators=[validate_no_special_chars])

    def clean(self):
        data = super().clean()
        # cross-field validation...
        return data
```

```python
# app/admin.py
from django.contrib import admin
from .models import ExtractionConfig
from .forms import ExtractionConfigForm

@admin.register(ExtractionConfig)
class ExtractionConfigAdmin(admin.ModelAdmin):
    form = ExtractionConfigForm
    list_display = ('name', 'source', 'last_run')
    readonly_fields = ('last_run',)
    actions = ['run_now']

    @admin.action(description='Run selected')
    def run_now(self, request, queryset):
        for obj in queryset:
            obj.run_extraction(triggered_by=request.user, enqueue=True)
        self.message_user(request, f"Queued {queryset.count()} jobs.")
```

---

# 16. When to stop customizing forms

* Prefer simplicity: only add complexity if you need cross-field validation, dynamic fields, or special presentation.
* If you find yourself adding many UI behaviors, consider a front-end SPA with APIs and use serializers for validation.
