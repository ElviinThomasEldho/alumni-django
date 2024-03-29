from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('profile/', views.profile, name="profile"),
    path('view-profile/<int:id>/', views.viewProfile, name="viewProfile"),
    path('feed/', views.feed, name="feed"),
    path('follow/<int:id>/', views.followAccount, name="followAccount"),
    path('unfollow/<int:id>/', views.unfollowAccount, name="unfollowAccount"),
    path('create-post/', views.createPost, name="createPost"),
    path('like-post/<int:id>/', views.likePost, name="likePost"),
    # Authentication
    path('login/', views.loginUser, name="loginUser"),
    path('logout/', views.logoutUser, name="logoutUser"),
    path('register/', views.registerUser, name="register"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
