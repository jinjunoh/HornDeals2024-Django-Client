from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
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
    # revealing username (for useronly delete)
    user = serializers.ReadOnlyField(source='user.username')
    voted = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False)
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
            return obj.voters.filter(id=request.user.id).exists()
        return False

    def get_seller_name(self, obj):
        return obj.user.username
    
# serializer.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image']  # we only need image for now

class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'image']

    def get_image(self, obj):
        try:
            return self.context['request'].build_absolute_uri(obj.profile.image.url)
        except:
            return None
