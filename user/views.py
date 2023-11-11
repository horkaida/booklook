from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse


def get_user(request):
    return render(request, 'user/user.html', {})

def get_user_history(request):
    return render(request, 'user/history.html', {})



def get_wishlist(request):
    #if post - remove from wishlist
    return render(request, 'books/wishlist.html', {})

def get_already_read_list(request):
    #if post - remove from already read
    return render(request, 'books/already_read.html', {})


def get_favourites(request):
    #if post - remove from fav
    # return redirect('/')
    return render(request, 'books/favourites.html', {})


def log_in(request):
    if request.method=='GET':
        return render(request, 'user/login.html')
    if request.method=='POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(f'USER {user}')
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'user/login.html', {'error':'Incorrect credentials!'})

def register(request):
    if request.method=='GET':
        return render(request, 'user/registration.html')
    if request.method=='POST':
        if request.POST.get('password') == request.POST.get('repeat_password'):
            user = User.objects.create_user(username=request.POST.get('username'),
                                            email=request.POST.get('email'),
                                            password=request.POST.get('password'))
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
            return redirect('/login')
        else:
            return render(request, 'user/registration.html', {'error':'Паролі не співпадають.'})