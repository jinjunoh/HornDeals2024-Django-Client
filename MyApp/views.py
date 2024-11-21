from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

@csrf_exempt
def login_MyApp(request):
    """
    Handle user login.
    Expects 'username' and 'password' in POST request body.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful', 'username': user.username}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'POST request required'}, status=405)


@csrf_exempt
def logout_user(request):
    """
    Handle user logout.
    """
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)

    return JsonResponse({'error': 'POST request required'}, status=405)

def login_view(request):
    # Handle login logic here
    return JsonResponse({'message': 'Login endpoint reached'})

def logout_view(request):
    """Logs out the user and returns a success message."""
    logout(request)
    return JsonResponse({'message': 'Successfully logged out'}, status=200)

@api_view(['GET'])
def sample_view(request):
    return Response({"message": "Hello, world!"})

@api_view(['GET'])
def get_users(request):
    user = User.objects.get(username="testuser")
    return Response({"message": user.username})