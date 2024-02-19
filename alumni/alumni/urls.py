from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('main/', include('main.urls')),
    path('rooms/', include('room.urls')),  # Include the 'room' app URLs under 'rooms/'
]
