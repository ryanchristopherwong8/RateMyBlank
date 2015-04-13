from django.shortcuts import render
from src.models.ratedmodel import RatedModel
from src.models.ratedobject import RatedObject
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

def show(request, ratedModelName, ratedModelId, ratedObjectName, ratedObjectId):
    current_user = request.user
    ratedobject = RatedObject.objects.get(pk = ratedObjectId)
    return render(request, 'ratedobject.html', {"ratedobject": ratedobject, "current_user": current_user})

def create(request, ratedModelName, ratedModelId):
    ratedobjectname = request.POST['name']
    dt = datetime.now()
    df = DateFormat(dt)
    ratedobject = RatedObject(name = ratedobjectname, rated_model_id = ratedModelId,
        created_at = df.format('Y-m-d'))
    ratedobject.save()
    url = reverse('ratedobjectshow', kwargs={'ratedModelName' : ratedModelName, 'ratedModelId' : ratedModelId,
        'ratedObjectName' : ratedobject.name.replace(" ", ""), 'ratedObjectId' : str(ratedobject.id)})
    return HttpResponseRedirect(url)