from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

from .models import Product

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']  # Renamed here

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],  
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

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
