
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booklook.settings')


app = Celery('booklook')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
     'calc_avg_rate':{
         'task': 'books.tasks.calc_average_book_rate',
         'schedule': crontab(minute='*/1')
     }
}
app.conf.timezone = 'UTC'

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

