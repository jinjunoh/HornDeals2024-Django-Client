from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Product
from .serializer import ProductSerializer, SignUpSerializer, LoginSerializer
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework import status

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
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'User created successfully',
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login successful',
                'token': token.key
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid email or password'
            }, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def filter_products(request):
    data = request.data
    category = data.get('category', '')
    price_range = data.get('priceRange', [0, 999999999])
    sort_by = data.get('sortBy', 'latest')  # Default to 'latest'
    
    queryset = Product.objects.all()
    
    if category:
        queryset = queryset.filter(category=category)
        
    if len(price_range) == 2:
        min_price, max_price = price_range
        queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
    
    # Order the queryset based on the sort option
    if sort_by == 'latest':
        queryset = queryset.order_by('-created_at')  # newest posts first
    elif sort_by == 'popular':
        queryset = queryset.order_by('-popularity')  # most popular posts first

    serializer = ProductSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user

    if request.method == 'GET':
        # Use the correct field name: "user" instead of "owner"
        products = Product.objects.filter(user=user)
        favorites = Product.objects.filter(voters=user)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        favorites_serializer = ProductSerializer(favorites, many=True, context={'request': request})
        user_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return Response({
            'user': user_data,
            'products': serializer.data,
            'favorites': favorites_serializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = request.data
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.save()

        updated_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return Response({
            'message': 'Profile updated successfully',
            'user': updated_data
        }, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def product_detail(request, product_id):
    print("DEBUG: request.user =", request.user)
    print("DEBUG: is_authenticated =", request.user.is_authenticated)
    product = get_object_or_404(Product, id=product_id)
    print("DEBUG: product.voters =", product.voters.all())

    product.views += 1
    product.save()
    
    serializer = ProductSerializer(product, context={'request': request})
    data = serializer.data
    print("DEBUG: serializer output =", data)
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_popularity(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    if product.voters.filter(pk=user.pk).exists():
        product.popularity -= 1
        product.voters.remove(user)
        voted = False
    else:
        product.popularity += 1
        product.voters.add(user)
        voted = True
    product.save()
    return Response({"popularity": product.popularity, "voted": voted}, status=status.HTTP_200_OK)
