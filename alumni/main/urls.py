from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile/', views.profile, name="profile"),
    path('view-profile/', views.viewProfile, name="viewProfile"),
    path('feed/', views.feed, name="feed"),
    # Authentication
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
]