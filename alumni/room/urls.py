from django.urls import path

from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('create/', views.create_room, name='create_room'),
    path('<slug:slug>/', views.room, name='room'),
    path('create_personal_room/<str:username>/', views.create_personal_room, name='create_personal_room'),
]