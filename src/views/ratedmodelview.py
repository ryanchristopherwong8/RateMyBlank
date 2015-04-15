from django.shortcuts import render

from src.models.ratedmodel import RatedModel
from src.models.ratedobject import RatedObject
from src.models.attribute import Attribute
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

#Show all
def index(request):
  current_user = request.user
  ratedmodels = RatedModel.objects.order_by("-created_at")
  return render(request, 'index.html', {"ratedmodels": ratedmodels, "current_user": current_user})

#Show one
def show(request, ratedModelName, ratedModelId):
  current_user = request.user
  ratedobjects = RatedObject.objects.filter(rated_model_id = ratedModelId).order_by("-created_at")
  ratedmodel = RatedModel.objects.get(pk=ratedModelId)
  return render(request, 'ratedmodel.html', {"ratedobjects": ratedobjects, "current_user": current_user, "ratedmodel": ratedmodel})

#Show form for submitting
def submit(request):
  current_user = request.user
  return render(request, 'submit_ratedmodel.html', {"current_user": current_user})

#create new models
def create(request):
  attributeList = request.POST.getlist('attribute')
  dt = datetime.now()
  df = DateFormat(dt)
  ratedmodel = RatedModel(name = request.POST['name'], created_at = df.format('Y-m-d'))
  ratedmodel.save()

  for i in attributeList:
    attribute = Attribute(name = i, rated_model_id = ratedmodel.id)
    attribute.save()

  url = reverse('ratedmodelshow', kwargs={'ratedModelName' : ratedmodel.name.replace(" ",""), 'ratedModelId' : str(ratedmodel.id)})
  return HttpResponseRedirect(url)
