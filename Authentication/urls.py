from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import  RegisterView,logout_view,your_index_view
from .views import api_login_view, web_login_view, your_index_view, logout_view


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
   # path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout_view, name='logout'),

     path('api/login/', api_login_view, name='api_login'),  # API login URL
    path('login/', web_login_view, name='web_login'),      # Web login URL
    path('index/', your_index_view, name='index')
]
