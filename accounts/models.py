from django.contrib.auth.models import AbstractUser
from django.db import models
from userprofile.models import Profile
from django.contrib.auth import password_validation
from read_book.models import Book

class User(AbstractUser):
    nickname = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True)  
    profile=models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    past_read = models.ManyToManyField(Book, blank=True, related_name='book_past_read')
    cur_read = models.ManyToManyField(Book, blank=True, related_name='book_cur_read')
    favourite = models.ManyToManyField(Book, blank=True, related_name='book_favourite')
    balance = models.IntegerField(default=0, blank=True, null=True)
    purchased_books = models.ManyToManyField(Book, blank=True)
    left_read = models.ManyToManyField(Book, blank=True, related_name='book_left_read')

    def save(self, *args, **kwargs):
        try:
            profileid=self.profile.id
        except:
            profile=Profile.objects.create()
            self.profile=profile
            profile.save()
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None