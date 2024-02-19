from django.shortcuts import render, HttpResponse, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'main/login.html')


def registerUser(request):
    return render(request, 'main/register.html')

def logoutUser(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'main/home.html')


def profile(request):
    return render(request, 'main/profile.html')


def viewProfile(request):
    return render(request, 'main/viewProfile.html')


def feed(request):
    return render(request, 'main/feed.html')