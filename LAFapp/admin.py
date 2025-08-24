from django.contrib import admin
from .models import Items
# Register your models here.

class ItemsAdmin(admin.ModelAdmin):
  list_display = ("status", "description", "location", "email", "category", "key_word", "date")
  search_fields = ("status", "description", "key_word")
  
admin.site.register(Items, ItemsAdmin)
