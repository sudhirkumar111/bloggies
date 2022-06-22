from django.db import models
import datetime
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    
    title = models.CharField(max_length=200)
    desc = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)