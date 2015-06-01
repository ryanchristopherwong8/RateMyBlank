from django.db import models
from datetime import datetime

from src.models.userprofile import UserProfile
from src.models.ratedobject import RatedObject

class Review(models.Model):
    userprofile = models.ForeignKey(UserProfile)
    ratedobject = models.ForeignKey(RatedObject)
    created_at = models.DateField(default=datetime.now, max_length=200)
    description = models.TextField(max_length=2000, blank=True)
    is_deleted = models.BooleanField(default=False)