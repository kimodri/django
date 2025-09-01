from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser

# def remove_usable_password(add_fieldsets):
#     return tuple(
#         (section, {
#             key: tuple(field for field in value if field != 'usable_password') if key == 'fields' else value
#             for key, value in config.items()
#         })
#         for section, config in add_fieldsets
#     )

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = [
        "email",
        "username",
        "name",
        "is_staff",
    ]

    # This works because it's only for existing users
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("name",)}),)

    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("name",)}),)

admin.site.register(CustomUser, CustomUserAdmin)