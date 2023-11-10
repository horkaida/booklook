from django.urls import path
from books import views

urlpatterns = [
    path('', views.get_all_books, name='get_all_books'),
    path('<book_id>', views.get_book_preview, name='get_book_preview'),
    path('<book_id>/fav', views.add_to_favourites, name='add_to_favourites'),
    path('<book_id>/wish', views.add_to_wishlist, name='add_to_wishlist'),
    path('<book_id>/done', views.mark_as_read, name='mark_as_read'),
    path('<book_id>/open', views.open_book, name='open_book'),
    path('<book_id>/start', views.start_reading, name='start_reading'),
    path('<book_id>/stop', views.stop_reading, name='stop_reading'),
    path('<book_id>/rate', views.rate_book, name='rate_book'),
    path('feedbacks', views.get_feedbacks, name='get_feedbacks'),
    path('feedbacks/<feedback_id>', views.get_feedback, name='get_feedback'),
    path('genres', views.get_all_genres, name='get_all_genres'),
]