from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Create your models here.

MOOD_CHOICES = [
        ("HAPPY", "Happy"),
        ("CALM", "Calm"),
        ("SAD", "Sad"),
        ("BORED", "Bored"),
        ("ANXIOUS", "Anxious"),
        ("ANGRY", "Angry"),
    ]

class Mood(models.Model):
  title = models.CharField(max_length=7, choices=MOOD_CHOICES)
  content = models.TextField(default="")
  date = models.DateTimeField(timezone.now, default=timezone.now)

  def __str__(self):
        return self.title
  
  def get_absolute_url(self):
      return reverse("detail", kwargs={"mood_id": self.pk})
  
  
  
class Song(models.Model):
  title = models.CharField()
  artist = models.CharField()
  Hyperlink = models.CharField()
  url = models.CharField(max_length=200)
  mood = models.CharField(max_length=7, choices=MOOD_CHOICES)
  def __str__(self):
        return self.title
  

class CustomUser(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(_("email address"), unique=True)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  date_joined = models.DateTimeField(default=timezone.now)
  favorites = models.ManyToManyField(Song, default=list)

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = []

  objects = CustomUserManager()

  def __str__(self):
    return self.email

  
  
  



