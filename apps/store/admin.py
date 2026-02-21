from django.contrib import admin
from .models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'is_available', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)