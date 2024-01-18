from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User
=======
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
>>>>>>> fbd75cf519ffbbcaaeec54ecabded96cc12f902d

# Create your models here.

class Song(models.Model):
  title = models.CharField()
  artist = models.CharField()
  mp3_file = models.FileField(upload_to='mp3_files/')
  Hyperlink = models.CharField()

class Mood(models.Model):
  title = models.CharField()
  playlist = {models.ForeignKey(Song, on_delete=models.CASCADE, ), }


class CustomUser(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(_("email address"), unique=True)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  date_joined = models.DateTimeField(default=timezone.now)
  favorites = models.ManyToManyField(Song, default={'',})

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = []

  objects = CustomUserManager()

  def __str__(self):
    return self.email



