from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateField(max_length=200)