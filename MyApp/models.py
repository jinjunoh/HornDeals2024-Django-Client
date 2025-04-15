from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from storages.backends.s3boto3 import S3Boto3Storage

s3 = S3Boto3Storage()

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('tickets', 'Tickets'),
        ('studyMaterials', 'Study Materials'),
        ('miscellaneous', 'Sublease'),
        ('sublease', 'Miscellaneous'),
    )

    # post information
    title = models.CharField(max_length=200, default="Default Title")
    content = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # ForeignKey to link a Post to a specific User and Product
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    # get_user_model() used for default to populate existing entries in database..may need change later
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1)
    
    # product information
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        blank=True
    )
    image = models.ImageField(upload_to='products/', null=True, blank=True, storage=s3)
    popularity = models.IntegerField(default=0)
    voters = models.ManyToManyField(get_user_model(), related_name="voted_products", blank=True)

    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="additional_images")
    image = models.ImageField(upload_to='products/additional_images/', storage=s3)

    def __str__(self):
        return f"Image for {self.product.name}"