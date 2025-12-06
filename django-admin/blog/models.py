# blog/models.py
from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories" # Fixes the "Categorys" typo in Admin

    def __str__(self):
        return self.name

class Post(models.Model):
    # Options for the status dropdown
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    title = models.CharField(max_length=100)
    # Slug is used for the URL (e.g., my-first-post)
    slug = models.SlugField(max_length=250, unique_for_date='created_at')
    
    # Connecting to Category. PROTECT prevents deleting a category if it has posts.
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, default=1
    )
    
    content = models.TextField()
    
    # The status field using the choices defined above
    options = models.CharField(max_length=10, choices=options, default='draft')
    
    # Auto-add the date when created
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title