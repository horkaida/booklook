from books.utils import paginate
from django.db import models

from blog import models

from django.shortcuts import render

def get_all_posts(request, page_number=1):
    all_posts = models.BlogPost.objects.all().order_by('-date')
    page_number = request.GET.get('page') if request.GET.get('page') else page_number
    page_obj = paginate(page_number=page_number, data=all_posts, per_page=12)
    return render(request, 'blog/index.html', {'page_obj':page_obj})


def get_one_post(request, post_id):
    post = models.BlogPost.objects.filter(id=post_id).first()
    return render(request, 'blog/post.html', {'post':post})

