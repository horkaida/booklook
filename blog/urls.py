from django.urls import path

from blog import views

urlpatterns = [
    path('', views.get_main_page, name='get_main_page'),
]