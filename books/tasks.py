
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from books import models


@shared_task
def calc_average_book_rate():
    all_rates = models.Rate.objects.all()
    all_books = models.Book.objects.all()
    for book in all_books:
        rates_summ = 0
        rates_count = 0
        for rate in all_rates:
            if book.id == rate.book_id_id:
                rates_summ += rate.rate
                rates_count += 1
        if rates_count:
            models.Book.objects.filter(id=book.id).update(average_rate=rates_summ/rates_count)
        else:
            models.Book.objects.filter(id=book.id).update(average_rate=0)

