from django.shortcuts import render
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from src.models.ratedmodel import RatedModel
from src.models.ratedobject import RatedObject
from src.models.attribute import Attribute
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class RatedModelForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    dt = datetime.now()
    df = DateFormat(dt)
    created_at = forms.DateField(widget = forms.HiddenInput(), initial = df.format('Y-m-d'))
    class Meta:
        model = RatedModel
        fields = ('name', 'created_at')

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

#create new models
def create(request):
  context = RequestContext(request)
  if request.method == "POST":
    form = RatedModelForm(request.POST)
    if form.is_valid():
      ratedmodel = form.save(commit=True)
      attributeList = request.POST.getlist('attribute')
      for i in attributeList:
        attribute = Attribute(name = i, rated_model_id = ratedmodel.id)
        attribute.save()
      url = reverse('ratedmodelshow', kwargs={'ratedModelName' : ratedmodel.name.replace(" ",""), 'ratedModelId' : str(ratedmodel.id)})
      return HttpResponseRedirect(url)
  else:
    current_user = request.user
    form = RatedModelForm()
    return render_to_response('submit_ratedmodel.html', {"current_user": current_user, "form": form}, context)

