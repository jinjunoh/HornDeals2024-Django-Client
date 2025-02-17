from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from MyApp.models import Product 
from MyApp.serializer import ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['GET'])  # Ensure that only GET requests are allowed
def get_categories(request):
    """
    Return the list of product categories from Product model.
    This view doesn't use `request` data as it just returns static category choices.
    """
    categories = [{"value": category[0], "label": category[1]} for category in Product.CATEGORY_CHOICES]
    return Response(categories)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_product(request):
    """
    Create a new product.
    Expects JSON data like:
    {
        "title": "Post Title",
        "name": "Product Name",
        "price": 199.99,
        "location": "Some Location",
        "category": "clothing",
        "image": <image_file>
    }
    """
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_products(request):
    """
    Get a list of all products.
    Optionally, you can filter products by query parameters.
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_product(request, pk):
    """
    Get single product by its ID.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['PUT'])
def update_product(request, pk):
    """
    Update existing product.
    {
      "name": "Updated Product Name",
      "price": 150.00,
      "location": "Updated Location",
      "category": "accessories",
      "image": <image_file>
    }
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_product(request, pk):
    """
    Delete by ID.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
    
    product.delete()
    return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    