from django.db import models

class RatedModel(models.Model):
    name = models.CharField(max_length=200)
    created_date = models.DateField(max_length=200, auto_now_add=True)