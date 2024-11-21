from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
 # accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .models import User

@api_view(['GET'])
def sample_view(request):
    return Response({"message": "Hello, world!"})


@api_view(['GET'])
def get_users(request):
    user = User.objects.get(username="testuser")
    return Response({"message": user.username})


