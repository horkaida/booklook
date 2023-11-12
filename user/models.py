from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    avatar = models.TextField(null=True)
    def get_absolute_url(self):
        return '/user'

