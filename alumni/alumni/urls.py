from django.contrib import admin
from django.urls import path, include
from room import routing as room_routing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('', include('main.urls')),
    path('rooms/', include('room.urls')),
    path('ws/', include(room_routing.websocket_urlpatterns)),
]
