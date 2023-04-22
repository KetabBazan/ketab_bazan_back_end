import jinja2.meta
from django.db import models
from accounts.models import User
# Create your models here.


class UserActivity(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=10)
    action_id = models.IntegerField()

    def create(self, user, type, action_id):
        self.user = user
        self.type = type
        self.action_id = action_id
        self.save()
