# Foreign Key
A `ForeignKey` is a way to create a relationship between two tables in a database. It links a field in one model to the primary key of another model. Think of it like a cross-reference in a book: it tells you where to find related information in another section.

In the example of a `Post` model and a `CustomUser` model, the `ForeignKey` tells the database that each post "belongs to" a specific user.

## How It Works

### 1\. The `Post` Model and `CustomUser` Model

  * **`Post` Model:** This model stores information about a blog post, such as its `title` and `body`.
  * **`CustomUser` Model:** This model stores information about a user, such as their `username`, `email`, and `name`. Each user has a unique ID, which is their **primary key**.

### 2\. Creating the Relationship

To link a `Post` to an `Author`, you add a `ForeignKey` field to the `Post` model. This field will store the **primary key** of the `CustomUser` who wrote the post.

When Django creates the database tables, it adds a column to the `Post` table called `author_id`. This column contains the unique ID of the user who wrote the post, creating a direct link between the two tables.

### 3\. Resolving the Model

The `ForeignKey` needs to know which model it's linking to. You can provide this in two ways:

  * **Direct Model Class:** `models.ForeignKey(CustomUser, ...)`
    This works, but it can cause **circular import errors** if your `accounts` app needs to import models from the app where `Post` is defined.

  * **String Reference:** `models.ForeignKey('accounts.CustomUser', ...)`
    This is the recommended way. Django's app registry can look up the `CustomUser` model from this string at runtime.

### 4\. Using `settings.AUTH_USER_MODEL`

Using `settings.AUTH_USER_MODEL` is a special case of the string reference. It's a best practice for `ForeignKey` relationships with the user model. In your `settings.py` file, you can specify which model is your project's user model, for example:

```python
# settings.py
AUTH_USER_MODEL = 'accounts.CustomUser'
```

When Django sees `ForeignKey(settings.AUTH_USER_MODEL, ...)`, it checks this setting, reads the string `'accounts.CustomUser'`, and resolves it to the correct `CustomUser` model class. This approach makes your code more flexible and easier to maintain if you ever need to change your user model in the future.