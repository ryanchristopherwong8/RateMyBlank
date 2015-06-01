from django.shortcuts import render
from src.models.ratedmodel import RatedModel
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

#Show all
def create(request):
    if request.method == "POST":
      tag_name = request.POST['search']
      current_user = request.user
      url = reverse('tagview_index', kwargs={'tag_name' : tag_name})
      return HttpResponseRedirect(url)

def index(request, tag_name):
    current_user = request.user
    ratedmodels = RatedModel.objects.filter(tags__slug = tag_name)
    return render(request, 'index.html', {"ratedmodels": ratedmodels, "current_user": current_user})