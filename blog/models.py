from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    tag_id = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
