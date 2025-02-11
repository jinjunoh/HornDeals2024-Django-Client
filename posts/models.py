from django.db import models
from MyApp.models import User, Product  # Import the User and Product models from your friend's app

class Post(models.Model):
    # things for the post
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # ForeignKey to link a Post to a specific User and Product
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.title
