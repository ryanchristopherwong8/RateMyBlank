from django.db import models

from src.models.ratedmodel import RatedModel

class Attribute(models.Model):
    name = models.CharField(max_length=200)
    rated_model = models.ForeignKey(RatedModel)