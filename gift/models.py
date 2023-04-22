from django.db import models
from accounts.models import User
from read_book.models import Book
# Create your models here.


class GiftHistory(models.Model):
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='receiver')
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    message = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now=True)
