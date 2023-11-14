from django.db.models import Min
from django.db.models import Count
from django.shortcuts import render, redirect
from books import models
from books.utils import (get_books_properties,calc_total_reading,
                         get_all_genres, paginate, get_one_book_properties)
from datetime import datetime, timedelta, date, timezone
from django.contrib.auth.decorators import login_required

def get_main_page(request):
    most_popular_books = models.Book.objects.order_by('-average_rate').all()[:8]
    last_feedbacks = models.Feedback.objects.order_by('-created_at').all()[:4]
    if request.user.is_authenticated:
        user_books = models.BookInUse.objects.all().filter(user_id_id=request.user.id)
        most_popular_books = get_books_properties(most_popular_books, user_books)
    return render(request, 'index.html', {'most_popular_books':most_popular_books,
                                          'last_feedbacks':last_feedbacks,
                                          'all_genres':get_all_genres()})


def get_all_books(request, page_number=1):
    all_books = models.Book.objects.all()
    page_number = request.GET.get('page') if request.GET.get('page') else page_number
    page_obj = paginate(data=all_books, page_number=page_number)
    if request.user.is_authenticated:
        user_books = models.BookInUse.objects.all().filter(user_id_id=request.user.id)
        page_obj = get_books_properties(page_obj, user_books)
        return render(request, 'books/books.html', {'page_obj':page_obj,
                                                'all_genres':get_all_genres()})
    return render(request, 'books/books.html', {'page_obj': page_obj,
                                                'all_genres': get_all_genres()})


def get_all_books_by_genre(request, genre_id, page_number=1):
    all_books = models.Book.objects.all().filter(genre_id=genre_id)
    page_number = request.GET.get('page') if request.GET.get('page') else page_number
    page_obj = paginate(data=all_books, page_number=page_number)
    if request.user.is_authenticated:
        user_books = models.BookInUse.objects.all().filter(user_id_id=request.user.id)
        page_obj = get_books_properties(page_obj, user_books)
        return render(request, 'books/books.html', {'page_obj':page_obj,
                                                'all_genres':get_all_genres()})
    return render(request, 'books/books.html', {'page_obj': page_obj,
                                                'all_genres': get_all_genres()})



def get_book_preview(request, book_id, page_number=1):
    current_book = models.Book.objects.get(id=book_id)
    if request.user.is_authenticated:
        user_book = models.BookInUse.objects.filter(book_id_id=book_id,
                                                 user_id_id=request.user.id).first()
        if user_book:
            if user_book.book_id_id == current_book.id:
                current_book = get_one_book_properties(current_book, user_book)
    book_feedbacks = models.Feedback.objects.all().filter(book_id_id=book_id)
    page_number = request.GET.get('page') if request.GET.get('page') else page_number
    page_obj = paginate(page_number=page_number, data=book_feedbacks, per_page=10)
    return render(request, 'books/book_preview.html',{'book':current_book,
                                                      'all_genres':get_all_genres(),
                                                      'page_obj':page_obj})

def search(request, page_number=1):
    if request.method == 'POST':
        search_query = request.POST['search_query']
        all_books = models.Book.objects.filter(title__contains=search_query)
        page_number = request.GET.get('page') if request.GET.get('page') else page_number
        page_obj = paginate(data=all_books, page_number=page_number)
        if request.user.is_authenticated:
            user_books = models.BookInUse.objects.all().filter(user_id_id=request.user.id)
            page_obj = get_books_properties(page_obj, user_books)
        return render(request, 'books/search_result.html', {'query':search_query, 'page_obj':page_obj})
    else:
        return render(request, 'books/search_result.html',{})

def open_book(request, book_id): #TODO Add to render last reading session by this book
    book = models.Book.objects.get(id=book_id)
    last_reading_session = models.ReadingSession. objects.filter(user_id_id=request.user.id,
                                                                   book_id_id=book_id).last()
    return render(request, 'books/book.html', {'book':book,
                                               'all_genres':get_all_genres(),
                                               'last_reading_session':last_reading_session})


@login_required(login_url='/user/login')
def start_reading(request, book_id): #TODO DO  OT ALLOW NEW START IF PREVIOUS IS NOT STOPPED
    book = models.Book.objects.get(id=book_id)
    current_book_in_use = models.BookInUse.objects.filter(book_id_id=book_id,
                                                          user_id_id=request.user.id).first()
    if current_book_in_use: #WRITE FIRST START READING TIME TO DB
        models.BookInUse.objects.filter(book_id_id=book_id).update(status_id=1)
        if not current_book_in_use.start_reading:
            models.BookInUse.objects.filter(book_id_id=book_id).update(start_reading=datetime.now(timezone.utc))
    else:
        models.BookInUse.objects.create(book_id_id=book_id,
                                        user_id_id=request.user.id,
                                        status_id=2,
                                        start_reading=datetime.now(timezone.utc))
    reading_session = models.ReadingSession.objects.create(book_id_id=book_id,
                                                           user_id_id=request.user.id,
                                                           start_reading_time=datetime.now(timezone.utc))
    return redirect(open_book, book_id=book_id)


@login_required(login_url='/user/login')
def stop_reading(request, book_id):
    stop_reading_time = datetime.now(timezone.utc)
    book_in_use = models.BookInUse.objects.filter(user_id_id=request.user.id,
                                                         book_id_id=book_id).first()
    if book_in_use:
        current_total_reading = book_in_use.total_reading_time
        if not book_in_use.total_reading_time:
            current_total_reading = 0
    else:
        current_total_reading = 0
    last_reading_session = models.ReadingSession. objects.filter(user_id_id=request.user.id,
                                                                        book_id_id=book_id).last()
    if last_reading_session and not last_reading_session.end_reading_time:

        total_reading_time = calc_total_reading(current_total_time=current_total_reading,
                                                stop_reading=stop_reading_time,
                                                start_reading=last_reading_session.start_reading_time)
        models.ReadingSession.objects.filter(id=last_reading_session.id).update(end_reading_time=stop_reading_time)
        models.BookInUse.objects.filter(user_id_id=request.user.id,book_id_id=book_id).update(total_reading_time=total_reading_time)

    return redirect(open_book, book_id=book_id)


@login_required(login_url='/user/login')
def add_to_favourites(request, book_id):
    current_book_in_use = models.BookInUse.objects.filter(book_id_id=book_id,
                                                          user_id_id=request.user.id).first()
    if current_book_in_use:
        models.BookInUse.objects.filter(book_id_id=book_id,
                                        user_id_id=request.user.id).update(is_favourite=False if current_book_in_use.is_favourite else True)
    else:
        models.BookInUse.objects.create(book_id_id=book_id,
                                        user_id_id=request.user.id,
                                        is_favourite=True)
    return redirect(f'/books/{book_id}')


@login_required(login_url='/user/login')
def mark_as_read(request, book_id):  #SHOW IN TEMPLATE ONLY IF LOGGED
    current_book_in_use = models.BookInUse.objects.filter(book_id_id=book_id,
                                                          user_id_id=request.user.id).first()
    if current_book_in_use:
        models.BookInUse.objects.filter(book_id_id=book_id,
                                        user_id_id=request.user.id).update(status_id=3 if current_book_in_use.status_id==2 else 2)
    else:
        models.BookInUse.objects.create(book_id_id=book_id,
                                        user_id_id=request.user.id,
                                        status_id=2)
    return redirect(f'/books/{book_id}')


@login_required(login_url='/user/login')
def add_to_wishlist(request, book_id):
    if request.user.is_authenticated: #SHOW IN TEMPLATE ONLY IF LOGGED
        current_book_in_use = models.BookInUse.objects.filter(book_id_id=book_id,
                                                              user_id_id=request.user.id).first()
        if current_book_in_use:
            models.BookInUse.objects.filter(book_id_id=book_id,
                                            user_id_id=request.user.id).update(is_wishlist=False if current_book_in_use.is_wishlist else True)
        else:
            models.BookInUse.objects.create(book_id_id=book_id,
                                            user_id_id=request.user.id,
                                            is_wishlist=True)
    return redirect(get_book_preview, book_id=book_id)


@login_required(login_url='/user/login')
def add_feedback(request):
    if request.method=='POST':
        text = request.POST.get('text')
        book_id = request.POST.get('book_id')
        models.Feedback.objects.create(user_id_id=request.user.id,
                                       book_id_id=book_id,
                                       text=text)
        return redirect(get_book_preview, book_id=book_id)


@login_required(login_url='/user/login')
def remove_feedback(request, feedback_id):
    current_feedback = models.Feedback.objects.filter(id=feedback_id,
                                                      user_id_id=request.user.id).first()
    if current_feedback:
        models.Feedback.objects.filter(id=feedback_id).delete()
        return redirect(get_book_preview, book_id=current_feedback.book_id_id)

def get_genres(request):
    all_genres = get_all_genres()
    return render(request, 'books/genres.html', {'all_genres':all_genres})


@login_required(login_url='/user/login')
def rate_book(request, book_id):
    book_rate = request.POST.get('book_rate')
    rated_book = models.Rate.objects.filter(user_id_id=request.user.id,
                                            book_id_id=book_id).first()
    if rated_book:
        models.Rate.objects.filter(user_id_id=request.user.id,
                                   book_id_id=book_id).update(rate=book_rate)
    else:
        new_rate = models.Rate.objects.create(user_id_id=request.user.id,
                                          book_id_id=book_id,
                                          rate=book_rate)
    return redirect(f'/books/{book_id}')





