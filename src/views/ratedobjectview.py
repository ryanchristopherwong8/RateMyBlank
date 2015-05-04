from django.shortcuts import render
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from src.models.ratedmodel import RatedModel
from src.models.ratedobject import RatedObject
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

class RatedObjectForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    class Meta:
        model = RatedObject
        fields = ('name', 'description')

def show(request, ratedmodel_name, ratedmodel_id, ratedobject_name, ratedobject_id):
    current_user = request.user
    ratedobject = RatedObject.objects.get(pk=ratedobject_id)
    return render(request, 'ratedobject_show.html', {"ratedobject": ratedobject, "current_user": current_user})

def create(request, ratedmodel_name, ratedmodel_id):
    context = RequestContext(request)
    try:
        ratedmodel = RatedModel.objects.get(pk=ratedmodel_id)
    except RatedModel.DoesNotExist:
        return HttpResponse('<h1>Page was not found</h1>')
    if request.method == "POST":
        ratedobject_form = RatedObjectForm(request.POST)
        if ratedobject_form.is_valid():
            ratedobject = ratedobject_form.save(commit=False)
            ratedobject.ratedmodel_id = ratedmodel_id
            ratedobject.save()
            url = reverse('ratedobject_show', kwargs={'ratedmodel_name' : ratedmodel_name, 'ratedmodel_id' : ratedmodel_id,
                'ratedobject_name' : ratedobject.name.replace(" ", ""), 'ratedobject_id' : str(ratedobject.id)})
            return HttpResponseRedirect(url)
        print(ratedobject_form.errors)
    else:
        ratedobject_form = RatedObjectForm()
    current_user = request.user
    return render_to_response('ratedobject_create.html', {"current_user": current_user, "ratedobject_form": ratedobject_form, "ratedmodel": ratedmodel}, context)