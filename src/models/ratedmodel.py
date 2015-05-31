from django.db import models
from datetime import datetime
from taggit.managers import TaggableManager

class RatedModel(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateField(default=datetime.now, max_length=200)
    description = models.TextField(max_length=1000, blank=True)
    tags = TaggableManager()