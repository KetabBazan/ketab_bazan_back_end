from django.db import models
from accounts.models import User
from read_book.models import Genre


class Group(models.Model):
    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=250, blank=True)
    picture = models.ImageField(default="groupimages/default.jpg", upload_to='groupimages')
    users = models.ManyToManyField(User, blank=True)
    category = models.ForeignKey(to=Genre, on_delete=models.CASCADE)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='owner')


class ChatMessage(models.Model):
    message = models.CharField(max_length=500, null=False, blank=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, unique=False)
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
