from django.urls import path
from .views import contact, register ,login,user_profile_view

urlpatterns = [ 
path('register/',register),    
path('login/', login),
path('contact/',contact),
path('user-profile',user_profile_view),
]
