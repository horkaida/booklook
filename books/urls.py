from django.urls import path
from books import views

urlpatterns = [
    path('', views.get_main_page, name='get_main_page'),
    path('books/', views.get_all_books, name='get_all_books'),
    path('books/genres', views.get_genres, name='get_genres'),
    path('books/feedbacks', views.get_feedbacks, name='get_feedbacks'),
    path('books/feedbacks/<feedback_id>', views.get_feedback, name='get_feedback'),
    path('books/<book_id>', views.get_book_preview, name='get_book_preview'),
    path('books/<book_id>/fav', views.add_to_favourites, name='add_to_favourites'),
    path('books/<book_id>/wish', views.add_to_wishlist, name='add_to_wishlist'),
    path('books/<book_id>/done', views.mark_as_read, name='mark_as_read'),
    path('books/<book_id>/open', views.open_book, name='open_book'),
    path('books/<book_id>/start', views.start_reading, name='start_reading'),
    path('books/<book_id>/stop', views.stop_reading, name='stop_reading'),
    path('books/<book_id>/rate', views.rate_book, name='rate_book')
]