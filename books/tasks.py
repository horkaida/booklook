from celery import app
from celery.schedules import crontab
from books import models
from django.db.models import Count

CELERYBEAT_SCHEDULE = {
   'calc_average_book_rate': {
       'task': 'calc_average_book_rate',
       'schedule': crontab(minute='1')}
}


@app.task(name='calc_average_book_rate')
def calc_average_book_rate():
    all_rates = models.Rate.objects.all()
    all_books = models.Book.objects.all()
    for book in all_books:
        rates_summ = 0
        rates_count = 0
        for rate in all_rates:
            if book.id == rate.book_id:
                rates_summ += rate.rate
                rates_count += 1
        if rates_count:
            models.Book.objects.filter(id=book.id).update(average_rate=rates_summ/rates_count)
        else:
            models.Book.objects.filter(id=book.id).update(average_rate=0)
    print('CELERY WORKED!!!!')

