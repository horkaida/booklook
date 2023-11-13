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
    # last_reviewed_books = models.Feedback.objects.values('book_id_id').distinct()
    #
    # for book in last_reviewed_books:
    #     print(book)
    # page_number = request.GET.get('page')
    # page_obj = paginate(all_books, page_number)
    return render(request, 'index.html', {'most_popular_books':most_popular_books,
                                          'last_feedbacks':last_feedbacks,
                                          'all_genres':get_all_genres()})


def get_all_books(request, page_number=1):
    all_books = models.Book.objects.all()
    if request.GET.get('page'):
        page_number = request.GET.get('page')
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
    if request.GET.get('page'):
        page_number = request.GET.get('page')
    page_obj = paginate(all_books, page_number)
    if request.user.is_authenticated:
        user_books = models.BookInUse.objects.all().filter(user_id_id=request.user.id,
                                                           genre_id=genre_id)
        page_obj = get_books_properties(page_obj, user_books)
        return render(request, 'books/books.html', {'page_obj':page_obj,
                                                'all_genres':get_all_genres()})
    return render(request, 'books/books.html', {'page_obj': page_obj,
                                                'all_genres': get_all_genres()})

@login_required(login_url='/user/login')
def mark_as_read(request, book_id):
    if request.user.is_authenticated:   #SHOW IN TEMPLATE ONLY IF LOGGED
        current_book_in_use = models.BookInUse.objects.filter(book_id_id=book_id,
                                                              user_id_id=request.user.id).first()
        if current_book_in_use:
            models.BookInUse.objects.filter(book_id_id=book_id,
                                            user_id_id=request.user.id).update(status_id=2)
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
                                            user_id_id=request.user.id).update(is_wishlist=True)
        else:
            models.BookInUse.objects.create(book_id_id=book_id,
                                            user_id_id=request.user.id,
                                            is_wishlist=True)
        return redirect('user/wishlist')
    return redirect('user/wishlist')

def get_book_preview(request, book_id, page_number=1):
    current_book = models.Book.objects.get(id=book_id)
    if request.user.is_authenticated:
        user_book = models.BookInUse.objects.filter(book_id_id=book_id,
                                                 user_id_id=request.user.id).first()
        if user_book:
            if user_book.book_id_id == current_book.id:
                current_book = get_one_book_properties(current_book, user_book)
    book_feedbacks = models.Feedback.objects.all().filter(book_id_id=book_id)
    if request.GET.get('page'):
        page_number = request.GET.get('page')
    page_obj = paginate(page_number, book_feedbacks, 10)
    return render(request, 'books/book_preview.html',{'book':current_book,
                                                      'all_genres':get_all_genres(),
                                                      'page_obj':page_obj})

def search(request, page_number=1):
    if request.method == 'POST':
        search_query = request.POST['search_query']
        all_books = models.Book.objects.filter(title__contains=search_query)
        page_number = request.GET.get('page')
        page_obj = paginate(all_books, page_number)
        if request.user.is_authenticated:
            user_books = models.BookInUse.objects.all().filter(user_id_id=request.user.id)
            page_obj = get_books_properties(page_obj, user_books)
        return render(request, 'books/search_result.html', {'query':search_query, 'page_obj':page_obj})
    else:
        return render(request, 'books/search_result.html',{})

def open_book(request, book_id): #TODO Add to render last reading session by this book
    book = models.Book.objects.get(id=book_id)
    return render(request, 'books/book.html', {'book':book,
                                               'all_genres':get_all_genres()})


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
    last_reading_session = models.ReadingSession.objects.filter(user_id_id=request.user.id,
                                                                   book_id_id=book_id).last()
    total_reading_time = calc_total_reading(current_total_time=current_total_reading,
                                            stop_reading=stop_reading_time,
                                            start_reading=last_reading_session.start_reading_time)
    models.ReadingSession.objects.filter(id=last_reading_session.id).update(end_reading_time=stop_reading_time)
    models.BookInUse.objects.filter(user_id_id=request.user.id,book_id_id=book_id).update(total_reading_time=total_reading_time)

    return redirect(open_book, book_id=book_id)


@login_required(login_url='/user/login')
def add_to_favourites(request, book_id):
    current_book_in_use = models.BookInUse.objects.filter(book_id_id=book_id,
                                                          user_id_id=request.user.id)
    if current_book_in_use:
        models.BookInUse.objects.filter(book_id_id=book_id,
                                        user_id_id=request.user.id).update(is_favourite=True)
    else:
        models.BookInUse.objects.create(book_id_id=book_id,
                                        user_id_id=request.user.id,
                                        is_favourite=True)
    return redirect(f'books/{book_id}')


def get_all_feedbacks(request, page_number=1):
    all_feedbacks = models.Feedback.objects.all()
    page_number = request.GET.get('page')
    page_obj = paginate(page_number, all_feedbacks, 20)
    return render(request, 'books/feedbacks.html', {'all_genres':get_all_genres(),
                                                    'page_obj':page_obj})

def get_feedback(request, feedback_id):
    #if post - remove feedback
    return render(request, 'books/feedback.html', {'all_genres':get_all_genres()})

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





