from django.db import models

from src.models.review import Review
from src.models.attribute import Attribute

class Score(models.Model):
    review = models.ForeignKey(Review, null=True)
    grade = models.DecimalField(max_digits=2, decimal_places=1)
    attribute = models.ForeignKey(Attribute, null=True)
    is_deleted = models.BooleanField(default=False)