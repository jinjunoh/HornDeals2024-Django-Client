from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.sample_view, name="sample-view")
]