from django.urls import path
from .views import contact, notice_update, notice_view, register ,login,user_profile_view,assignment_creation
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [ 
path('register/',register),    
path('login/', login),
path('contact/',contact),
path('user-profile/',user_profile_view),
path('notice/<int:id>/',notice_update),
path('notice/',notice_view),
path('assignment/',assignment_creation),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
