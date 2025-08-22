from django import forms
from .models import Items

class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['status', 'description', 'location', 'email', 'date', 'category', 'key_word']