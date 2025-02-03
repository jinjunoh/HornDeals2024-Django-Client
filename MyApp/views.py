from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
 # accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .models import User, Product
from .serializer import ProductSerializer

@api_view(['GET'])
def sample_view(request):
    return Response({"message": "Hello, world!"})


@api_view(['GET'])
def get_users(request):
    user = User.objects.get(username="testuser")
    return Response({"message": user.username})


@api_view(['POST'])
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