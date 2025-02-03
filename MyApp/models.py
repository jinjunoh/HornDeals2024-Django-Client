from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    utemail = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('tickets', 'Tickets'),
        ('studyMaterials', 'Study Materials'),
        ('miscellaneous', 'Miscellaneous'),
    )
    
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=100)
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        blank=True
    )
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name