from django.urls import path
from .views import contact, register ,login

urlpatterns = [ 
path('register/',register),    
path('login/', login),
path('contact/',contact)
]
