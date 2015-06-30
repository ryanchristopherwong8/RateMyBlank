from django.db import models
from datetime import datetime
from django.core.validators import MinLengthValidator

from src.models.userprofile import UserProfile
from src.models.ratedobject import RatedObject
from src.models.attribute import Attribute

class Review(models.Model):
    userprofile = models.ForeignKey(UserProfile)
    ratedobject = models.ForeignKey(RatedObject)
    created_at = models.DateField(default=datetime.now, max_length=200)
    description = models.TextField(max_length=2000, validators=[MinLengthValidator(10)])
    score = models.DecimalField(max_digits=2, decimal_places=1)
    attribute = models.ForeignKey(Attribute)
    is_deleted = models.BooleanField(default=False)