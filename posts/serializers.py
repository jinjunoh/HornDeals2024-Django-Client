from rest_framework import serializers
from .models import Product


# The Serializer is what converts data to JSON so that the frontend or client
# understands the Django model instances or querysets
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product  
        fields = ['id', 'name', 'price', 'category', 'image'] 