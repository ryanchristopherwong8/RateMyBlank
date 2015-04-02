from django.shortcuts import render
from src.models.user import User
import datetime

# Create your views here.
def index(request):
    users = User.objects.order_by("-created_at")
    now = datetime.datetime.now()
    return render(request, 'index.html', {"users": users, "year": now.year})