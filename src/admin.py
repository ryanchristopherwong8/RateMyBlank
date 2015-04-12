from django.contrib import admin

# Register your models here.
from src.models.userprofile import UserProfile
from src.models.ratedmodel import RatedModel
from src.models.attribute import Attribute
from src.models.ratedobject import RatedObject
from src.models.review import Review
from src.models.score import Score

admin.site.register(UserProfile)
admin.site.register(RatedModel)
admin.site.register(Attribute)
admin.site.register(RatedObject)
admin.site.register(Review)
admin.site.register(Score)