from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login




User = get_user_model()





# Register View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# Login
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username and password:
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            response_data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
            # Set tokens in cookies (optional, if you want to use cookies)
            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie('access', response_data['access'], httponly=True)
            response.set_cookie('refresh', response_data['refresh'], httponly=True)
            # Redirect to index page (update URL name or path)
            return redirect(reverse('index'))  # Ensure you have an 'index' URL in your urls.py
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

# Token Refresh View (JWT)
@api_view(['POST'])
def token_refresh_view(request):
    refresh_token = request.data.get('refresh')
    
    if refresh_token:
        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)






@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username and password:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('index')  # Redirect to the index page
        else:
            return Response({"error": "Invalid credentials"}, status=400)
    else:
        return Response({"error": "Username and password required"}, status=400)




def your_index_view(request):
    return render(request, 'index.html')  # Update with your actual template



@api_view(['POST'])
def logout_view(request):
    logout(request)  # Logs out the user by clearing their session
    return redirect('index')  # Redirect to index or login page





# API Login View
@api_view(['POST'])
def api_login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username and password:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

# Web Login View
def web_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to index page
        else:
            return render(request, 'login.html', {"error": "Invalid credentials"})
    return render(request, 'login.html')  # Show login form for GET requests
