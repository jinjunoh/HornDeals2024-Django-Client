from django.urls import path
from . import views
from .views import filter_products
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('api/', views.sample_view, name='sample-view'),
    path('api/signup/', views.signup, name='signup'),
    path('api/login/', views.login_view, name='login'),
    path('api/users', views.get_users, name='get_users'),
    path('api/filter-products/', filter_products, name='filter_products'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)