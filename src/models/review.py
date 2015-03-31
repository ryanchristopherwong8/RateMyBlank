from django.db import models

from src.models.user import User
from src.models.ratedobject import RatedObject

class Review(models.Model):
    reviewer = models.ForeignKey(User, null=True)
    rated_object = models.ForeignKey(RatedObject, null=True)