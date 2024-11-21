from django.urls import path
from . import views  # Import your views

urlpatterns = [
    # Add your authentication endpoints here, e.g.,
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/', views.sample_view, name='sample-view')
    path('api/users', views.get_users, name='get_users')
]