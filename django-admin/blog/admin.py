from django.contrib import admin
from . import models
from . import forms

# Register your models here.
# admin.site.register(models.Post)
admin.site.register(models.Category)

@admin.register(models.Post)
class postAdmin(admin.ModelAdmin):
    list_display = ('title', 'category',)

    fields = ['title', 'category']

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
    # fieldsets = (
    #     ('Main Content', {
    #         'fields': ('title', 'category', 'options')
    #     }),
    #     ('Advanced Options', {
    #         'classes': ('collapse',), # This makes the section clickable/collapsible
    #         'fields': ('slug',), 
    #     }),
    # )

    # Here is where you connect a form
    form = forms.PostAdminForm

# You are writing a new admin area here
class BlogAdminArea(admin.AdminSite):
    site_header = "Blog Admin Area"
    site_title = "Blogs"

blog_site = BlogAdminArea(name="BlogAdmin")

blog_site.register(models.Post)
blog_site.register(models.Category)