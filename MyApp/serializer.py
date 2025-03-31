from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Product, ProductImage

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['email']  # Set username to email
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    voted = serializers.SerializerMethodField()
    additional_images = ProductImageSerializer(many=True, read_only=True)
    seller_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            image_url = obj.image.url
            if request is not None:
                return request.build_absolute_uri(image_url)
            return image_url
        return ''
    
    def get_voted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.voters.all()
        return False
    
    def get_seller_name(self, obj):
        return obj.user.username