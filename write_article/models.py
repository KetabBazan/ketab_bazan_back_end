from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from read_book.models import Book

def upload_to(instance, filename):
    return 'articles/{filename}'.format(filename=filename)

class Article(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    created_jalali = models.CharField(max_length=100, blank=True, default='')
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField(blank=True, default='')
    summary = models.TextField(blank=True, default='')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to=upload_to, default='articles/default.jpg')
    book = models.ForeignKey(Book, blank=True, null=True, on_delete = models.SET_NULL)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title