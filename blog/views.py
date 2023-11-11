from django.db import models
from blog.models import BlogPost


from django.shortcuts import render

def get_main_page(request):
    return render(request, 'blog/index.html', {})


