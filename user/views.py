from books.utils import paginate #TODO REFACTOR LOCATION
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from books import models


def get_user(request):
    return render(request, 'user/user.html', {})

def get_user_history(request, page_number=1):
    # if request.user.is_authenticated:
    #     all_read_books = models.BookInUse.objects.all().filter(user_id_id=request.user.id,
    #                                                            status_id=2)
    #     page_number = request.GET.get('page')
    #     page_obj = paginate(page_number, all_read_books, 12)
    return render(request, 'user/history.html', {'page_obj':page_obj})



def get_wishlist(request, page_number=1):
    if request.user.is_authenticated:
        wishlist_books = models.BookInUse.objects.all().filter(user_id_id=request.user.id,
                                                               is_wishlist=True)
        if request.GET.get('page'):
            page_number = request.GET.get('page')
        page_obj = paginate(page_number, wishlist_books, 12)
    return render(request, 'user/wishlist.html', {'page_obj':page_obj})

def get_already_read_list(request):
    if request.user.is_authenticated:
        wishlist_books = models.BookInUse.objects.all().filter(user_id_id=request.user.id,
                                                               status_id=2)
        if request.GET.get('page'):
            page_number = request.GET.get('page')
        page_obj = paginate(page_number, wishlist_books, 12)
    return render(request, 'user/already_read.html', {'page_obj':page_obj})


def get_favourites(request):
    if request.user.is_authenticated:
        wishlist_books = models.BookInUse.objects.all().filter(user_id_id=request.user.id,
                                                               is_favourite=True)
        if request.GET.get('page'):
            page_number = request.GET.get('page')
        page_obj = paginate(page_number, wishlist_books, 12)
    return render(request, 'books/favourites.html', {'page_obj':page_obj})


def log_in(request):
    if request.method=='GET':
        return render(request, 'user/login.html')
    if request.method=='POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
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