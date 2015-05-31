from django.shortcuts import render
from src.models.ratedmodel import RatedModel


#Show all
def index(request):
    if request.method == "POST":
      searchTag = request.POST['search']
      current_user = request.user
      ratedmodels = RatedModel.objects.filter(tags__slug = searchTag)
      return render(request, 'index.html', {"ratedmodels": ratedmodels, "current_user": current_user})

#Currently works however, we need to redirect url with search in url
#Need to change code so that after searching you can click models
#Depending on if there is a result than show if not Show different URL " Nothing Search " look at rated object view