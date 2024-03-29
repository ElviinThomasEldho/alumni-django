from django.shortcuts import render, HttpResponse, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .decorators import *
from .models import *
from .forms import *

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
    return redirect('loginUser')


def home(request):
    return render(request, 'main/home.html')


@authenticated_user
def profile(request):
    account = Account.objects.get(user=request.user)
    posts = Post.objects.filter(account=account)
    recommendations = Account.objects.all().exclude(user=request.user).exclude(id__in=account.following.values_list('id'))

    
    context = {
        "account":account,
        "posts":posts,
        "recommendations":recommendations,
    }
    return render(request, 'main/profile.html', context)

@authenticated_user
def viewProfile(request, id):
    account = Account.objects.get(id=id)
    posts = Post.objects.filter(account=account)
    recommendations = Account.objects.all().exclude(id=account.id)
    if account in Account.objects.get(user=request.user).followers.all():
        followed = True
    
    context = {
        "account":account,
        "posts":posts,
        "recommendations":recommendations,
        "followed":followed
    }
    return render(request, 'main/viewProfile.html', context)


@authenticated_user
def followAccount(request, id):
    account = Account.objects.get(user=request.user)
    target = Account.objects.get(id=id)
    account.following.add(target)
    target.followers.add(target)
    return redirect('profile')


@authenticated_user
def unfollowAccount(request, id):
    account = Account.objects.get(user=request.user)
    target = Account.objects.get(id=id)
    account.following.remove(target)
    target.followers.remove(target)
    return redirect('profile')

@authenticated_user
def createPost(request):
    form = PostForm()
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            post.account = Account.objects.get(user=request.user)
            post.save()

            return redirect("feed")

    
    context = {
        'form':form
    }
    
    return render(request, "main/createPost.html", context)
    
@authenticated_user
def likePost(request, id):
    post = Post.objects.get(id=id)
    account = Account.objects.get(user=request.user)
    post.likes.add(account)    
    return redirect('feed')

@authenticated_user
def feed(request):
    account = Account.objects.get(user=request.user)
    posts = Post.objects.all().order_by('-date_created')
    recommendations = Account.objects.all().exclude(user=request.user).exclude(id__in=account.following.values_list('id'))
    
    if request.method == 'POST':
        id = request.POST.get('id')
        title = request.POST.get('title')
        print(id, title)
        
        comment = Comment.objects.create(account=account, text=title)
        post = Post.objects.get(id=id)
        post.comments.add(comment)
    
    context = {
        "account":account,
        "posts":posts,
        "recommendations":recommendations,
    }
    
    return render(request, 'main/feed.html', context)