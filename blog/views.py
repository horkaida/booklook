from books.utils import paginate #TODO REFACTOR LOCATION
from django.db import models

from blog import models


from django.shortcuts import render

def get_all_posts(request, page_number=1):
    all_posts = models.BlogPost.objects.all().order_by('-date')
    if request.GET.get('page'):
        page_number = request.GET.get('page')
    page_obj = paginate(page_number, all_posts, 12)
    return render(request, 'blog/index.html', {'page_obj':page_obj})


