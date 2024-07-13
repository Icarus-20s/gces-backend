from django.urls import path
from .views import contact, notice_update, notice_view, register ,login,user_profile_view

urlpatterns = [ 
path('register/',register),    
path('login/', login),
path('contact/',contact),
path('user-profile/',user_profile_view),
path('notice/<int:id>/',notice_update),
path('notice/',notice_view)
]
