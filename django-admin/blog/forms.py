# blog/forms.py
from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostAdminForm(forms.ModelForm):
    # 1. Customizing a widget or help text without changing the Model
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'special-css-class'}),
        help_text="Please enter a catchy title (Admin only note)."
    )

    class Meta:
        model = Post
        fields = '__all__'

    # 2. Custom Validation Logic
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title.isupper():
            raise ValidationError("Please do not use ALL CAPS in the title.")
        return title