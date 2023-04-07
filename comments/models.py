from django.db import models
from accounts.models import User



# Create your models here.
from read_book.models import Book


class Comment(models.Model):
    comment_text = models.CharField(max_length=500, null=False, blank=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, unique=False)
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return "username: " + self.user.username + "book:" + self.book.name + "comment: " + self.comment_text[:7]


class Replycomment(models.Model):
    reply_text = models.CharField(max_length=500, null=False, blank=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "user:" + self.user.username + "reply:" + self.reply_text[:7]
