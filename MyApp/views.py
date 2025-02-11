from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .models import User, Product
from .serializer import ProductSerializer, SignUpSerializer, LoginSerializer
from django.contrib.auth import authenticate , login
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes

@api_view(['GET'])
def sample_view(request):
    return Response({"message": "Hello, world!"})


@api_view(['GET'])
def get_users(request):
    user = User.objects.get(username="testuser")
    return Response({"message": user.username})


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Create or retrieve the token associated with this user
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'User created successfully',
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    if not serializer.is_valid():
        print(serializer.errors)  # <-- Quick debugging
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        # Grab email & password from the validated data
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # If you're using Django's default user model, you can authenticate by username OR email
        # Adjust as needed if your User model uses email as the USERNAME_FIELD
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Retrieve or create the token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login successful',
                'token': token.key
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid email or password'
            }, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)@api_view(['POST'])

def filter_products(request):
    """
    Expects JSON data like:
    {
      "category": "clothing",
      "priceRange": [50, 200],
      "locations": ["gregoryGym", "eer"]
    }
    """
    data = request.data
    
    category = data.get('category', '')           # e.g. "clothing"
    price_range = data.get('priceRange', [0, 999999999])
    locations = data.get('locations', [])         # e.g. ["gregoryGym", "eer"]

    queryset = Product.objects.all()
    
    # Filter by category if provided
    if category:
        queryset = queryset.filter(category=category)
    
    # Filter by price range if provided
    if len(price_range) == 2:
        min_price, max_price = price_range
        queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
    
    # Filter by locations if provided
    if locations:
        queryset = queryset.filter(location__in=locations)
    
    serializer = ProductSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)