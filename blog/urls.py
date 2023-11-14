from django.urls import path

from blog import views

urlpatterns = [
    path('', views.get_all_posts, name='get_all_posts'),
    path('<post_id>', views.get_one_post, name='get_one_post')
]