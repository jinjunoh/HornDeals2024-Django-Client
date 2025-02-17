from django.contrib import admin
from MyApp.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  pass