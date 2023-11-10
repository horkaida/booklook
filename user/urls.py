from django.urls import path
from django.conf import settings
from django.contrib.auth.views import LogoutView
from user import views


urlpatterns = [
    path('', views.get_user, name='get_user'),
    path('user/history', views.get_user_history, name='get_user_history'),
    path('readlist', views.get_already_read_list, name='get_already_read_list'),
    path('favourites', views.get_favourites, name='get_favourites'),
    path('wishlist', views.get_wishlist, name='get_wishlist'),
    path('login', views.log_in, name='log_in'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('register', views.register, name='register'),
]