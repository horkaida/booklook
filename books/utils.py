from django.core.paginator import Paginator

from books import models


def get_books_properties(page_obj, user_books):
    for book in page_obj:
        for user_book in user_books:
            if book.id == user_book.book_id_id and user_book.is_favourite:
                book.liked = True
            if book.id == user_book.book_id_id and user_book.is_wishlist:
                book.wishlist = True
            if book.id == user_book.book_id_id and user_book.status_id == 2:
                book.done = True
    return page_obj

def get_one_book_properties(current_book, user_book):
    current_book.liked = user_book.is_favourite
    current_book.wishlist = user_book.is_wishlist
    if user_book.status_id == 2:
        current_book.done = True
    return current_book


def get_all_genres():
    all_genres = models.Genre.objects.all()
    return all_genres


def paginate(page_number, data, per_page = 12):
    paginator = Paginator(data, per_page)
    page_object = paginator.get_page(page_number)
    return page_object

def calc_total_reading(current_total_time, stop_reading, start_reading):
    #stop_reading:datetime, start_reading:datetime
    time_per_session = stop_reading - start_reading
    days_from_session = time_per_session.days
    hours_from_session = time_per_session.seconds//3600
    minutes_from_session = (time_per_session.seconds//60)%60
    minutes_per_session = hours_from_session*60 + minutes_from_session + days_from_session*24*60
    total_time = minutes_per_session + int(current_total_time)
    return total_time

