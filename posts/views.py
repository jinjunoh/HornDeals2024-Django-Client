from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from MyApp.models import Product, ProductImage
from MyApp.serializer import ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from random import sample
from rest_framework.permissions import IsAuthenticated

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
@permission_classes([IsAuthenticated])
def create_product(request):
    """
    Create a new product with multiple images.
    Expects multipart/form-data with the following structure:
    {
        "title": "Post Title",
        "name": "Product Name",
        "price": 199.99,
        "category": "accessories",
        "image": <image_file>,
        "additional_images": [<image_file1>, <image_file2>, ...] (optional, up to 5)
    }
    """
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save(user=request.user)

            # Handle multiple additional images
            additional_images = request.FILES.getlist('additional_images')
            for img in additional_images[:5]:  # Restrict to a max of 5 images
                ProductImage.objects.create(product=product, image=img)

            return Response(ProductSerializer(product, context={'request': request}).data, status=status.HTTP_201_CREATED)
        
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_logged_in_user(request):
    return Response({"username": request.user.username})

@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if product.user != request.user:
        return Response({"message": "You are not authorized to delete this product."}, status=status.HTTP_403_FORBIDDEN)

    product.delete()
    return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def related_products(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    # Get products from the same category, excluding the current product
    related = list(Product.objects.filter(category=product.category).exclude(id=pk))

    # If there are fewer than 3 related products, fill the remaining spots
    if len(related) < 3:
        additional_products = list(Product.objects.exclude(id=pk).exclude(id__in=[p.id for p in related]))
        needed = 3 - len(related)
        
        if len(additional_products) >= needed:
            related += sample(additional_products, needed)
        else:
            related += additional_products  # Take all available if less than needed

    # Ensure exactly 3 products are returned
    related = related[:3]

    serializer = ProductSerializer(related, many=True)
    return Response(serializer.data)