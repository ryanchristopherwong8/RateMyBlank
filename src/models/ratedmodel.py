from django.db import models

# Create your models here.
class RatedModel(models.Model):
    name = models.CharField(max_length=200)
    publish_date = models.DateField(max_length=200)

class Attribute(models.Model):
    name = models.CharField(max_length=200)
    score = models.DecimalField(max_digits=2, decimal_places=1)
    rated_model = models.ForeignKey(RatedModel, null=True)

class RatedObject(models.Model):
    name = models.CharField(max_length=200)
    publish_date = models.DateField(max_length=200)
    rated_model = models.ForeignKey(RatedModel, null=True)