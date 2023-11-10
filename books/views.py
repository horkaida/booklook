from django.shortcuts import render, redirect
from booklook.wsgi import *
from books import models
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from books.utils import get_books_properties, get_one_book_properties
from datetime import datetime, timedelta, date, timezone

def get_all_books(request, page_number=1):
    all_books = models.Book.objects.all()
    paginator = Paginator(all_books, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        user_books = models.BookInUse.objects.all().filter(user_id_id=request.user.id)
        page_obj = get_books_properties(page_obj, user_books)
    return render(request, 'books/books.html', {'page_obj':page_obj})

def mark_as_read(request, book_id):
    if request.user.is_authenticated:   #SHOW IN TEMPLATE ONLY IF LOGGED
        current_book_in_use = models.BookInUse.objects.filter(book_id=book_id,
                                                              user_id_id=request.user.id)
        if current_book_in_use:
            current_book_in_use.update(status_id=3)
        else:
            models.BookInUse.objects.create(book_id_id=book_id,
                                            user_id_id=request.user.id,
                                            status_id=3)
        return redirect(f'/books/{book_id}')

def add_to_wishlist(request, book_id):
    if request.user.is_authenticated: #SHOW IN TEMPLATE ONLY IF LOGGED
        current_book_in_use = models.BookInUse.objects.filter(book_id=book_id,
                                                              user_id_id=request.user.id)
        if current_book_in_use:
            current_book_in_use.update(status_id=1)
        else:
            models.BookInUse.objects.create(book_id_id=book_id,
                                            user_id_id=request.user.id,
                                            status_id=1)
    return render(request, 'user/favourites.html', {})

def get_book_preview(request, book_id):
    current_book = models.BookInUse.objects.filter(book_id=book_id)
    user_books = models.BookInUse.objects.all().filter(user_id_id=request.user.id)
    current_book = get_one_book_properties(current_book, user_books)
    return render(request, 'books/book_preview.html', {'current_book':current_book})

def search():
    pass

def open_book(request, book_id):
    current_book = models.BookInUse.objects.filter(book_id=book_id)
    return render(request, 'books/book.html', {'current_book':current_book})


def start_reading(request, book_id):
    if request.user.is_authenticated: #SHOW IN TEMPLATE ONLY IF LOGGED
        current_book_in_use = models.BookInUse.objects.filter(book_id=book_id,
                                                              user_id_id=request.user.id)
        if current_book_in_use:
            current_book_in_use.update(status_id=2,
                                       start_reading=datetime.now(timezone.utc))
        else:
            models.BookInUse.objects.create(book_id_id=book_id,
                                            user_id_id=request.user.id,
                                            status_id=2,
                                            start_reading=datetime.now(timezone.utc))


    return render(request, 'books/book.html', {})

def stop_reading(request, book_id):
    redirect('/') #to book_preview


def add_to_favourites(request, book_id):
    # return redirect('/') #redirect to fav page
    return render(request, 'books/favourites.html', {})


def get_feedbacks(request):
    # if post - add feedback
    return render(request, 'books/feedbacks.html', {})


def get_feedback(request, feedback_id):
    #if post - remove feedback
    return render(request, 'books/feedback.html', {})

def get_all_genres(request):
    return render(request, 'books/genres.html', {})


def rate_book(request, book_id):
    return render(request, 'books/book.html', {})





