from books.utils import paginate #TODO REFACTOR LOCATION
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from books import models
from django.views.generic import UpdateView
from user.models import CustomUser

#TODO CHANGE LOGIN LOGOUT REGISTER URLS
class ProfileUpdateView(UpdateView):
    model = CustomUser
    template_name = 'user/edit_profile.html'
    fields = ['first_name', 'last_name'] #TODO CHANGE TO FORM CLASS


@login_required(login_url='/user/login')
def get_user(request):
    all_read_books = models.BookInUse.objects.all().filter(user_id_id=request.user.id,
                                                            status_id=2).order_by('-id')
    all_added_to_fav = models.BookInUse.objects.all().filter(user_id_id=request.user.id,
                                                              is_favourite=True).order_by('-id')
    all_added_to_wishlist = models.BookInUse.objects.filter(user_id_id=request.user.id,
                                                                   is_wishlist=True).order_by('-id')
    user_data = {'all_read_books_count':len(all_read_books),
                 'all_favourites_count': len(all_added_to_fav),
                 'all_wishlist_count':len(all_added_to_wishlist),
                 'last_read_books':all_read_books[:4],
                 'last_added_to_fav':all_added_to_fav[:4],
                 'last_added_to_wishlist':all_added_to_wishlist[:4],}
    return render(request, 'user/user.html', {'user_data':user_data})



@login_required(login_url='/user/login') #TODO WITH BOOK PROPERTIES
def get_user_history(request, page_number=1):
    all_read_books = models.BookInUse.objects.all().filter(user_id_id=request.user.id, status_id__in=[1, 2])
    if request.GET.get('page'):
        page_number = request.GET.get('page')
    page_obj = paginate(page_number, all_read_books, 12)
    return render(request, 'user/history.html', {'page_obj':page_obj})


@login_required(login_url='/user/login')
def get_wishlist(request, page_number=1):
    wishlist_books = models.BookInUse.objects.all().filter(user_id_id=request.user.id,
                                                           is_wishlist=True)
    if request.GET.get('page'):
        page_number = request.GET.get('page')
    page_obj = paginate(page_number=page_number, data=wishlist_books, per_page=12)
    return render(request, 'user/wishlist.html', {'page_obj':page_obj})


@login_required(login_url='/user/login')
def get_favourites(request, page_number=1):
    wishlist_books = models.BookInUse.objects.all().filter(user_id_id=request.user.id,
                                                           is_favourite=True)
    if request.GET.get('page'):
        page_number = request.GET.get('page')
    page_obj = paginate(page_number, wishlist_books, 12)
    return render(request, 'user/favourites.html', {'page_obj':page_obj})


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
            user = CustomUser.objects.create_user(username=request.POST.get('username'),
                                            email=request.POST.get('email'),
                                            password=request.POST.get('password'))
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
            return redirect('/user/login')
        else:
            return render(request, 'user/registration.html', {'error':'Паролі не співпадають.'})