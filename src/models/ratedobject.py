from django.db import models

from src.models.ratedmodel import RatedModel

class RatedObject(models.Model):
    name = models.CharField(max_length=200)
    publish_date = models.DateField(max_length=200)
    rated_model = models.ForeignKey(RatedModel, null=True)