from django.contrib import admin

# Register your models here.
from src.models.user import User
 
admin.site.register(User)