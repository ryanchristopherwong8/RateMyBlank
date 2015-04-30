from django.db import models

from src.models.ratedmodel import RatedModel

class RatedObject(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateField(max_length=200)
    rated_model = models.ForeignKey(RatedModel)
    description = models.TextField(max_length=1000, blank=True)