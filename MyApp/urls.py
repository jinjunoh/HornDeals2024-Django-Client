from django.urls import path
from . import views
from .views import filter_products




urlpatterns = [
    path('api/', views.sample_view, name='sample-view'),
    path('api/users', views.get_users, name='get_users'),
    path('api/filter-products/', filter_products, name='filter_products'),
]