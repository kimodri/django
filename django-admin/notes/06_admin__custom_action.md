# **Custom Actions in Django Admin**

**Custom actions** allow you to define operations that can be performed on one or more selected rows in the admin list view.

* Admin automatically adds a dropdown above the table called **“Actions”**.
* You define the logic in Python, and Django handles calling it for the selected objects.

---

## 1. **Why use custom actions**

* You want admins to perform **bulk operations** on model instances.
* Example conceptual use cases:

  * “Run Now” → trigger a process on selected rows
  * “Mark as Published” → update a status field
  * “Export” → generate a file for selected objects
  * “Deactivate” → disable selected users

**Key point:** The action logic belongs in the admin, but it usually calls **model methods or services** to do the work.

---

## 2. **Defining a custom action**

You define a function inside your admin class (or outside and reference it).

```python
from django.contrib import admin

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')

    @admin.action(description="Run Now")
    def run_now(self, request, queryset):
        for obj in queryset:
            obj.run()  # Call a model method or service
```

### Key points:

* `self` → the admin class instance
* `request` → the current HTTP request
* `queryset` → all the selected objects from the admin table
* `@admin.action(description="…")` → optional decorator to set the label in the dropdown

---

## 3. **Connecting actions to the admin**

By default, actions listed in the admin class appear in the **actions dropdown**.

```python
class MyModelAdmin(admin.ModelAdmin):
    actions = ['run_now']  # list of action method names
```

* If `actions` is not defined, Django automatically picks up all methods decorated with `@admin.action`.
* When an admin selects one or more rows and chooses the action, Django calls the method with the selected objects.

---

## 4. **How custom actions run**

1. Admin sends a POST request with the selected object IDs and the action name.
2. Django calls the corresponding action method.
3. Inside the method, you usually iterate over `queryset` and perform the operation.
4. Optionally, return an **HttpResponse** or call `self.message_user()` to show a success message.

Example with a message:

```python
@admin.action(description="Run Now")
def run_now(self, request, queryset):
    for obj in queryset:
        obj.run()
    self.message_user(request, f"{queryset.count()} items were run successfully.")
```

---

## 5. **Relation to “Run Now” conceptually**

Even if your model represents “configs for extraction” or “tasks,” the **concept is the same**:

* You have objects in the table.
* Admin selects one or more objects.
* Your action triggers some process on those objects (call a method, enqueue a task, etc.).
* The method/action itself is separate from the model — it **calls model methods or services**.

---

## 6. **Tips for writing good custom actions**

1. **Use model methods for the actual work**: keep the admin action thin.

   ```python
   for obj in queryset:
       obj.run_now_task()  # Model or service handles the real work
   ```

2. **Support multiple objects**: always iterate over `queryset`, not single objects.

3. **Use `message_user`** to give feedback to the admin.

4. **Be careful with long-running tasks**: don’t block the admin request — consider Celery or background jobs.

5. **Use `@admin.action(description="…")`** instead of manually setting `short_description`.

---

### Summary

| Concept           | How it works                                                            |
| ----------------- | ----------------------------------------------------------------------- |
| **Action**        | A method in the admin class that operates on selected objects           |
| **Trigger**       | Admin selects rows, chooses the action from the dropdown, clicks “Go”   |
| **Arguments**     | `self` = admin, `request` = HTTP request, `queryset` = selected objects |
| **Use case**      | Bulk operations like “Run Now”, “Publish”, “Deactivate”, “Export”       |
| **Best practice** | Call model methods/services from the action, keep admin code thin       |

### Question:
> how does the admin send a post request is it after choosing in the dropdown above the table also please relate it to Extraction task for example your table is configs per row and you have this run button right, what do they look like in codes, for example this is a project ran with databricks

Yes — here’s a detailed explanation of **how Django admin sends the POST request** and how that connects conceptually to something like an “Extraction Task” table with a “Run Now” action. I’ll also show how it looks in code.


# 1. **How admin sends the POST request**

When you define a custom action:

1. In the **change list view** (the table of objects in the admin), above the table is a **dropdown menu** labeled “Action”.

2. Steps an admin user takes:

   * Select one or more rows (checkboxes on the left of the table).
   * Choose an action from the dropdown (e.g., “Run Now”).
   * Click **Go**.

3. Django admin **automatically generates a POST request** with:

   * The selected object IDs (via checkboxes).
   * The name of the action.
   * CSRF token and other metadata.

4. Django admin then **calls the corresponding action method** you defined, passing:

   * `request` → the current HTTP request object.
   * `queryset` → a QuerySet of the selected objects.

---

# 2. **Conceptual connection to Extraction Tasks**

Imagine your table is **ExtractionConfig**:

| Name     | Source | Status |
| -------- | ------ | ------ |
| Config 1 | DB1    | Ready  |
| Config 2 | DB2    | Ready  |

* Each row is a config for an extraction job (maybe run on Databricks).
* You want admins to select one or more configs and hit “Run Now”.
* The **action** triggers the job for each selected config.

---

# 3. **How the code looks**

```python
# models.py
class ExtractionConfig(models.Model):
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    last_run = models.DateTimeField(null=True, blank=True)

    def run_extraction(self):
        """
        Model method to execute the extraction job.
        Could call Databricks API or enqueue a background job.
        """
        # Pseudo-code: run the task
        print(f"Running extraction for {self.name} on source {self.source}")
        # self.last_run = timezone.now()
        # self.save()
```

```python
# admin.py
from django.contrib import admin
from .models import ExtractionConfig

@admin.register(ExtractionConfig)
class ExtractionConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'source', 'last_run')
    actions = ['run_now']

    @admin.action(description="Run Now")
    def run_now(self, request, queryset):
        """
        Custom admin action triggered from dropdown.
        queryset = selected ExtractionConfig rows.
        """
        for config in queryset:
            config.run_extraction()   # call the model method
        self.message_user(request, f"{queryset.count()} extraction(s) started.")
```

---

# 4. **Flow of the “Run Now” action**

1. Admin visits the **ExtractionConfig** table in Django admin.
2. Admin selects one or more configs using the checkboxes.
3. Admin chooses **Run Now** from the **Actions dropdown**.
4. Admin clicks **Go** → Django sends a **POST request** with the selected IDs and the action.
5. Django calls `run_now(self, request, queryset)`.
6. Inside `run_now`:

   * Iterate over `queryset` (selected rows).
   * Call `run_extraction()` for each config.
   * Optionally show a success message.

---

# 5. **What it would look like for a Databricks workflow**

* `run_extraction()` could:

```python
def run_extraction(self):
    from myapp.databricks import submit_job
    submit_job(config_name=self.name, source=self.source)
```

* Admin just selects rows → clicks “Run Now” → jobs are submitted to Databricks.
* The admin UI **never needs to know the implementation details**, it just triggers the model method.

---

# 6. **Key takeaways**

* **Django admin handles the POST request automatically.** You just define the action method.
* **Selected objects are passed as `queryset`.**
* Admin actions are ideal for “Run Now” / bulk operations because they work for multiple rows.
* The actual task execution logic belongs in the **model method** or a **service layer**, keeping the admin thin.

> how will you connect it to a logging table for instance, because now you don't have views but models

Exactly — when you’re doing actions entirely in the **admin**, there’s no view layer to log things by default. You can handle logging **directly in your model method** or in the admin action. Here’s how to think about it.

---

# 1. **Why you need a logging table**

For something like a “Run Now” extraction task:

* Each time a config is executed, you may want to log:

  * Which config ran
  * When it ran
  * Who triggered it
  * The status or result

Since there’s no view layer, **the model method or admin action is responsible for logging**.

---

# 2. **Create a logging model**

```python
from django.db import models
from django.contrib.auth.models import User

class ExtractionLog(models.Model):
    config = models.ForeignKey('ExtractionConfig', on_delete=models.CASCADE)
    triggered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    message = models.TextField(blank=True, null=True)
```

* This table will record every execution attempt.
* `triggered_by` can capture the admin user who clicked “Run Now”.

---

# 3. **Logging from the model method**

You can pass the user as an argument:

```python
class ExtractionConfig(models.Model):
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)

    def run_extraction(self, user=None):
        """
        Runs the extraction and logs the attempt.
        """
        from django.utils import timezone

        # Here you would run the real extraction logic
        success = True  # placeholder
        message = f"Extraction started for {self.name}"

        # Create a log record
        ExtractionLog.objects.create(
            config=self,
            triggered_by=user,
            timestamp=timezone.now(),
            status="Success" if success else "Failed",
            message=message
        )
```

---

# 4. **Admin action passes the user**

```python
@admin.register(ExtractionConfig)
class ExtractionConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'source')
    actions = ['run_now']

    @admin.action(description="Run Now")
    def run_now(self, request, queryset):
        for config in queryset:
            config.run_extraction(user=request.user)  # pass the admin user
        self.message_user(request, f"{queryset.count()} extraction(s) started and logged.")
```

* `request.user` is the admin who triggered the action.
* Logs are saved in the `ExtractionLog` table.
* This way, you **don’t need a view** — the admin action triggers both the execution and the logging.

---

# 5. **Key points**

* Admin actions are **essentially views under the hood**; they receive `request` and `queryset`.
* You can use `request.user` to identify who triggered the action.
* Logging can be done **inside the model method** or **inside the admin action**.
* This keeps your admin actions reusable, clean, and auditable.

