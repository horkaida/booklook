from books import models


def get_books_properties(page_obj, user_books): #TODO REFACTOR
    for book in page_obj:
        for user_book in user_books:
            if book.id == user_book.book_id_id and user_book.is_favourite:
                book.liked = True
            if book.id == user_book.book_id_id and user_book.status_id==1:
                book.wishlist = True
            if book.id == user_book.book_id_id and user_book.status_id == 3:
                book.done = True
    return page_obj

def get_one_book_properties(current_book, users_books):
    for user_book in users_books:
        if current_book.id == user_book.book_id_id and user_book.is_favourite:
            current_book.liked = True
        if current_book.id == user_book.book_id_id and user_book.status_id == 1:
            current_book.wishlist = True
        if current_book.id == user_book.book_id_id and user_book.status_id == 3:
            current_book.done = True
