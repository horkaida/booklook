from django.db.models import Min
from django.shortcuts import render, redirect
from books import models
from books.utils import (get_books_properties,
                         get_one_book_properties,
                         calc_total_reading, get_all_genres, paginate)
from datetime import datetime, timedelta, date, timezone


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

def mark_as_read(request, book_id):
    if request.user.is_authenticated:   #SHOW IN TEMPLATE ONLY IF LOGGED
        current_book_in_use = models.BookInUse.objects.filter(book_id_id=book_id,
                                                              user_id_id=request.user.id)
        if current_book_in_use:
            current_book_in_use.update(status_id=2)
        else:
            models.BookInUse.objects.create(book_id_id=book_id,
                                            user_id_id=request.user.id,
                                            status_id=2)
        return redirect(f'/books/{book_id}')

def add_to_wishlist(request, book_id):
    if request.user.is_authenticated: #SHOW IN TEMPLATE ONLY IF LOGGED
        current_book_in_use = models.BookInUse.objects.filter(book_id_id=book_id,
                                                              user_id_id=request.user.id)
        if current_book_in_use:
            current_book_in_use.update(is_wishlist=True)
        else:
            models.BookInUse.objects.create(book_id_id=book_id,
                                            user_id_id=request.user.id,
                                            is_wishlist=True)
        return redirect('user/wishlist')
    return redirect('user/wishlist')

def get_book_preview(request, book_id):
    current_book = models.BookInUse.objects.filter(book_id_id=book_id)
    if request.user.is_authenticated:
        user_book = models.BookInUse.objects.get(book_id_id=book_id,
                                                 user_id_id=request.user.id)
        if user_book:
            current_book = get_one_book_properties(current_book, user_book)
    book_feedbacks = models.Feedback.objects.all().filter(book_id_id=book_id)
    page_number = request.GET.get('page')
    page_obj = paginate(page_number, book_feedbacks, 20)
    return render(request, 'books/book_preview.html',{'current_book':current_book,
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

def open_book(request, book_id):
    current_book = models.BookInUse.objects.filter(book_id_id=book_id)
    return render(request, 'books/book.html', {'current_book':current_book,
                                               'all_genres':get_all_genres()})


def start_reading(request, book_id):
    if request.user.is_authenticated: #SHOW IN TEMPLATE ONLY IF LOGGED
        current_book_in_use = models.BookInUse.objects.filter(book_id_id=book_id,
                                                              user_id_id=request.user.id)
        if current_book_in_use:
            current_book_in_use.update(status_id=1)
            if not current_book_in_use.start_reading:
                current_book_in_use.update(start_reading=datetime.now(timezone.utc))
        else:
            models.BookInUse.objects.create(book_id_id=book_id,
                                            user_id_id=request.user.id,
                                            status_id=2,
                                            start_reading=datetime.now(timezone.utc))
        book_session = models.ReadingSession.objects.create(book_id_id=book_id,
                                                            user_id_id=request.user.id,
                                                            start_reading_time=datetime.now(timezone.utc))
        return book_session

def stop_reading(request, book_id):
    if request.user.is_authenticated:
        stop_reading_time = datetime.now(timezone.utc)
        current_total_reading = models.BookInUse.objects.get(user_id_id=request.user.id,
                                                             book_id_id=book_id)
        last_reading_session = models.ReadingSession.objects.filter(user_id_id=request.user.id,
                                                                       book_id_id=book_id).last()
        total_reading_time = calc_total_reading(current_total_time=current_total_reading,
                                                stop_reading=stop_reading_time,
                                                start_reading=last_reading_session.start_time)
        book_session = models.ReadingSession.objects.update(stop_reading=stop_reading_time,
                                             total_reading_time=total_reading_time)
        return book_session


def add_to_favourites(request, book_id):
    if request.user.is_authenticated:
        current_book_in_use = models.BookInUse.objects.filter(book_id_id=book_id,
                                                              user_id_id=request.user.id)
        if current_book_in_use:
            current_book_in_use.update(is_favourite=True)
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


def rate_book(request, book_id):
    if request.user.is_authenticated:
        book_rate = request.POST.get('book_rate')
        new_rate = models.Rate.objects.update(user_id_id=request.user.id,
                                              book_id_id=book_id,
                                              rate=book_rate)
    redirect('/')





