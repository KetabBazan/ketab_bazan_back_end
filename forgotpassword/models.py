from django.db import models
from django.dispatch import receiver
from django.shortcuts import render
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.conf import settings
# Create your models here.
