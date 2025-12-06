# Model Properties in Django

This covers **when to use them, how they run, how they differ from methods, and their connection with Django admin.**

---

## 1. What is a model property?

A **model property** is a method on your model class, decorated with `@property`, that behaves like an attribute.

* It **computes a value dynamically** based on other fields.
* It is **read-only** unless you define a setter.
* It **does not create a database column**.

Example:

```python
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = 0.12

    @property
    def price_with_tax(self):
        return self.price * (1 + self.tax_rate)
```

Usage:

```python
p = Product.objects.first()
print(p.price_with_tax)  # Computes the value on the fly
```

---

## 2. When to use model properties

Use a property when:

1. **The value is derived from existing fields**

   * `full_name = first_name + last_name`
   * `is_overdue = due_date < today`
   * `total_price = unit_price * quantity`

2. **The value should not be stored in the database**

   * It can be computed dynamically
   * Storing it would create redundant or inconsistent data

3. **You want attribute-like access**

   * Access it like `obj.full_name` instead of calling `obj.get_full_name()`

Example:

```python
@property
def full_name(self):
    return f"{self.first_name} {self.last_name}"
```

---

## 3. How model properties run

* A property runs **each time it is accessed**.
* Example:

```python
product.price_with_tax   # Executes the method body when accessed
```

* It does **not** run automatically; you access it using the dot operator.
* If it uses related objects, it may trigger database queries (watch for N+1 problems).

Optional: Use `@cached_property` to compute once per instance if the computation is expensive:

```python
from django.utils.functional import cached_property

@cached_property
def expensive_calculation(self):
    # Computed once, cached in the instance
    return complex_operation(self.data)
```

---

## 4. Difference between methods and properties

| Feature      | Method                                      | Property                                  |
| ------------ | ------------------------------------------- | ----------------------------------------- |
| Access       | `obj.method()`                              | `obj.property`                            |
| Arguments    | Can accept parameters                       | Cannot accept parameters (read-only)      |
| Side effects | Can modify instance or database             | Should be side-effect free                |
| Use case     | Actions or computations requiring arguments | Computed, derived, or attribute-like data |

**Rule of thumb:**

* Use **methods** for actions or computations requiring arguments.
* Use **properties** for simple derived data you want to access like an attribute.

---

## 5. Connection with Django Admin

* Properties can be used in `list_display` just like model fields or methods.
* Admin will **call the property automatically** for each row:

```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'price_with_tax')
```

* Django admin treats a property like a read-only field.
* If you want it sortable or want to give it a label, use `@admin.display` with methods instead:

```python
@admin.display(description="Price with Tax")
def price_with_tax_display(self, obj):
    return obj.price_with_tax
```

* Admin will call `price_with_tax_display(obj)` for each row.
* Properties are safer if you just want simple read-only computed data.

---

## 6. Summary

* **Properties**: computed, attribute-like, no DB column, run on access.
* **Methods**: callable, can have arguments, can perform actions, run when called.
* **Admin**: can automatically use properties or methods in `list_display` to show dynamic data.
* **Views**: access properties like attributes, call methods like normal functions.

