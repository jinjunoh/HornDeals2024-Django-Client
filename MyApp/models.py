from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # Any other fields you want

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # fields required when creating a superuser

    def __str__(self):
        return self.email
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