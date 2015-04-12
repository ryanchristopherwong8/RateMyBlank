from django.db import models

from src.models.userprofile import UserProfile
from src.models.ratedobject import RatedObject

class Review(models.Model):
    reviewer = models.ForeignKey(UserProfile)
    rated_object = models.ForeignKey(RatedObject)
    created_at = models.DateField(max_length=200)