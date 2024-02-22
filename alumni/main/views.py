from django.shortcuts import render, HttpResponse, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .decorators import *
from .models import *

# Create your views here.
@unauthenticated_user
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('feed')

        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'main/login.html')


def registerUser(request):
    return render(request, 'main/register.html')


@authenticated_user
def logoutUser(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'main/home.html')


@authenticated_user
def profile(request):
    return render(request, 'main/profile.html')


def viewProfile(request):
    return render(request, 'main/viewProfile.html')


@authenticated_user
def feed(request):
    account = Account.objects.get(user=request.user)
    
    context = {
        "account":account
    }
    
    return render(request, 'main/feed.html', context)