from django.db import models
from django.contrib.auth.models import User
# https://docs.djangoproject.com/en/1.7/ref/contrib/auth/#django.contrib.auth.models.User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)