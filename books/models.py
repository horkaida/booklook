from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    text = models.TextField()
    genre_id = models.ManyToManyField(Genre)
    author = models.CharField(max_length=200)
    media = models.TextField()
    average_rate = models.IntegerField(null=True)

    def __str__(self):
        return self.title


class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BookInUse(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    total_reading_time = models.FloatField(null=True)
    is_favourite = models.BooleanField(default=False)
    start_reading =  models.DateTimeField(auto_now_add=False, null=True)
    finish_reading = models.DateTimeField(auto_now_add=False, null=True)

    def __str__(self):
        return self.book_id.title


class ReadingSession(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_reading_time =  models.DateTimeField(auto_now_add=True)
    end_reading_time = models.DateTimeField(auto_now_add=True)


class Rate(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    rate = models.FloatField()


class Feedback(models.Model):
    text = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)





