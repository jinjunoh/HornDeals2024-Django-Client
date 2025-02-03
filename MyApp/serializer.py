from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            image_url = obj.image.url
            # If you have a request in the serializer context, build an absolute URL
            if request is not None:
                return request.build_absolute_uri(image_url)
            return image_url
        return ''  # or you can return a default image URL
