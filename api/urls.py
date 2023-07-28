from django.urls import path
from . import views
from django.urls import path
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('getRegisteredUser', views.getRegisteredUser, name="getRegisteredUser"),
    path('registerUser', views.registerUser, name='registerUser'),
    path('loginUser', views.loginUser, name='loginUser'),
    path('user/<int:id>', views.getUser, name='getUser'),
   
]