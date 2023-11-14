from books.utils import paginate
from django.db import models

from blog import models

from django.shortcuts import render

def get_all_posts(request, page_number=1):
    all_posts = models.BlogPost.objects.all().order_by('-date')
    print('pos', all_posts)
    page_number = request.GET.get('page') if request.GET.get('page') else page_number
    page_obj = paginate(page_number=page_number, data=all_posts, per_page=12)
    print('sdasd', page_obj)
    return render(request, 'blog/index.html', {'page_obj':page_obj})


