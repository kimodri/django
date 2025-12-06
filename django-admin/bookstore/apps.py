from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

# class BookstoreAdminConfig(AdminConfig):
#     default_site = "bookstore.admin.BookstoreAdmin"

class BookstoreConfig(AppConfig):
    name = 'bookstore'
