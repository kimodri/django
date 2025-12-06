# bookstore/models.py
from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True, help_text="13 Character ISBN number")
    
    # A book has one publisher (ForeignKey)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    
    # A book can have multiple authors (ManyToMany)
    authors = models.ManyToManyField(Author)
    
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title