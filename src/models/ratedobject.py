from django.db import models

from src.models.ratedmodel import RatedModel

class RatedObject(models.Model):
    name = models.CharField(max_length=200)
    created_date = models.DateField(max_length=200, auto_now_add=True)
    rated_model = models.ForeignKey(RatedModel, null=True)