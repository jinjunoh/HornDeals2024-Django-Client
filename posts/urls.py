from django.urls import path 
from . import views

app_name = "posts"

urlpatterns = [
    path('products/', views.get_products, name='get_products'),
    path('product/<int:pk>/', views.get_product, name='get_product'),
    path('products/create/', views.create_product, name='create_product'),
    path('api/categories/', views.get_categories, name='get_categories'),
    path('products/update/<int:pk>/', views.update_product, name='update_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('api/products/<int:pk>/related/', views.related_products, name = 'related_products')
]