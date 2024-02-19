from django.shortcuts import render, HttpResponse

# Create your views here.
def login(request):
    return HttpResponse('login')


def signup(request):
    return HttpResponse('signup')


def home(request):
    return HttpResponse('home')


def profile(request):
    return HttpResponse('profile')


def viewProfile(request):
    return HttpResponse('viewProfile')


def feed(request):
    return HttpResponse('feed')