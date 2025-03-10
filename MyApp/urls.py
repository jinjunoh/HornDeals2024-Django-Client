from django.urls import path
from . import views
from .views import filter_products, profile, toggle_popularity, product_detail
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('api/', views.sample_view, name='sample-view'),
    path('api/signup/', views.signup, name='signup'),
    path('api/login/', views.login_view, name='login'),
    path('api/users', views.get_users, name='get_users'),
    path('api/filter-products/', filter_products, name='filter_products'),
    path('api/profile/', profile, name='profile'),
    path("product/<int:product_id>/", product_detail, name="product_detail"),
    path("toggle-popularity/<int:product_id>/", toggle_popularity, name="toggle_popularity"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)