from django.urls import path
from django.conf import settings
from django.contrib.auth.views import LogoutView
from user import views


urlpatterns = [
    path('login', views.log_in, name='log_in'),
    path('logout', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('register', views.register, name='register'),
    path('history', views.get_user_history, name='get_user_history'),
    path('', views.get_user, name='get_user'),
    path('<int:pk>/update', views.ProfileUpdateView.as_view(), name='profile-update'),
]