from django.contrib import admin

# Register your models here.
from src.models.user import User
from src.models.ratedmodel import RatedModel
from src.models.ratedmodel import Attribute
from src.models.ratedmodel import RatedObject

admin.site.register(User)
admin.site.register(RatedModel)
admin.site.register(Attribute)
admin.site.register(RatedObject)