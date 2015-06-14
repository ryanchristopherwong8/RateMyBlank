from django.db import models
from datetime import datetime
from taggit.managers import TaggableManager

from src.models.userprofile import UserProfile

class RatedModel(models.Model):
    name = models.CharField(max_length=200)
    name_key = models.CharField(unique=True, max_length=200)
    created_at = models.DateField(default=datetime.now, max_length=200)
    description = models.TextField(max_length=1000, blank=True)
    creator = models.ForeignKey(UserProfile, null=True)
    tags = TaggableManager()
    is_deleted = models.BooleanField(default=False)