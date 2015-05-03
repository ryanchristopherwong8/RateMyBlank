from django.db import models
from datetime import datetime

from src.models.ratedmodel import RatedModel

class RatedObject(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateField(default=datetime.now, max_length=200)
    ratedmodel = models.ForeignKey(RatedModel)
    description = models.TextField(max_length=1000, blank=True)