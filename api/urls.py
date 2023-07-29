from django.urls import path
from . import views


urlpatterns = [
    path('getRegisteredUser', views.getRegisteredUser, name="getRegisteredUser"),
    path('registerUser', views.registerUser, name='registerUser'),
    path('loginUser', views.loginUser, name='loginUser'),
    path('user/<int:id>', views.getUser, name='getUser'),
    path('markspam', views.markNumberSpam, name="mark-number-spam"),
    path('phone_number/', views.getUsersUsingPhoneNumberOrName, name="getUsersUsingPhoneNumberOrName")
]