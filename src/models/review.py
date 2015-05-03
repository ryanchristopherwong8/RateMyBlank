from django.db import models

from src.models.userprofile import UserProfile
from src.models.ratedobject import RatedObject

class Review(models.Model):
    user = models.ForeignKey(UserProfile)
    ratedobject = models.ForeignKey(RatedObject)
    created_at = models.DateField(max_length=200)
    description = models.TextField(max_length=2000, blank=True)