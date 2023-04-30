from django.db import models
from accounts.models import User
from read_book.models import Genre
# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=250, blank=True)
    picture = models.ImageField(default="groupimages/default.jpg", upload_to='groupimages')
    users = models.ManyToManyField(User, blank=True)
    category = models.ForeignKey(to=Genre, on_delete=models.CASCADE)
