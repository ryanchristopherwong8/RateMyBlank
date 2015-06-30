from django.shortcuts import render
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from src.models.ratedmodel import RatedModel
from src.models.ratedobject import RatedObject
from src.models.attribute import Attribute
from src.models.review import Review
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.db.models import Avg
from src.helpers.application_helper import strip_non_alphanum

class RatedObjectForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    class Meta:
        model = RatedObject
        fields = ('name', 'description')

def show(request, ratedmodel_name_key, ratedobject_name, ratedobject_id):
    current_user = request.user
    ratedobject = RatedObject.objects.get(pk = ratedobject_id)
    ratedmodel = RatedModel.objects.get(name_key = ratedmodel_name_key, is_deleted=False)
    if not is_url_valid(ratedmodel, ratedobject_name, ratedobject):
        return HttpResponse('<h1>Page was not found</h1>')
    reviews = ratedobject.review_set.filter(is_deleted=False)
    attributes = ratedobject.ratedmodel.attribute_set.filter(review__ratedobject_id = ratedobject_id, review__is_deleted=False).annotate(avg_grade = Avg('review__score'))
    overall_grade = list(ratedobject.review_set.filter(is_deleted=False).aggregate(Avg('score')).values())[0]
    return render(request, 'ratedobject_show.html', {"ratedobject": ratedobject, "ratedmodel": ratedmodel, "reviews": reviews, "attributes": attributes,
        "overall_grade": overall_grade, "current_user": current_user})

def create(request, ratedmodel_name_key):
    if not request.user.is_authenticated():
        return redirect("login")
    context = RequestContext(request)
    try:
        ratedmodel = RatedModel.objects.get(name_key=ratedmodel_name_key)
    except RatedModel.DoesNotExist:
        return HttpResponse('<h1>Page was not found</h1>')
    if request.method == "POST":
        ratedobject_form = RatedObjectForm(request.POST)
        if ratedobject_form.is_valid():
            ratedobject = ratedobject_form.save(commit=False)
            ratedobject.ratedmodel_id = ratedmodel.id
            ratedobject.creator_id = request.user.userprofile.id
            ratedobject.save()
            url = reverse('ratedobject_show', kwargs={'ratedmodel_name_key' : ratedmodel_name_key,
                'ratedobject_name' : strip_non_alphanum(ratedobject.name), 'ratedobject_id' : str(ratedobject.id)})
            return HttpResponseRedirect(url)
        print(ratedobject_form.errors)
    else:
        ratedobject_form = RatedObjectForm()
    current_user = request.user
    return render_to_response('ratedobject_create.html', {"current_user": current_user, "ratedobject_form": ratedobject_form, "ratedmodel": ratedmodel}, context)

def edit(request, ratedmodel_name_key, ratedobject_name, ratedobject_id):
    if not request.user.is_authenticated():
        return redirect("login")
    ratedobject = RatedObject.objects.get(pk=ratedobject_id)
    ratedmodel = RatedModel.objects.get(name_key = ratedmodel_name_key, is_deleted=False)
    if not is_url_valid(ratedmodel, ratedobject_name, ratedobject):
        return HttpResponse('<h1>Page was not found</h1>')
    if request.user.userprofile.id != ratedobject.creator_id:
        url = reverse('ratedobject_show', kwargs={'ratedmodel_name' : ratedmodel_name, 'ratedobject_name' : ratedobject_name,
            'ratedobject_id' : ratedobject_id})
        return HttpResponseRedirect(url)
    context = RequestContext(request)
    if request.method == "POST":
        ratedobject_form = RatedObjectForm(request.POST)
        if ratedobject_form.is_valid():
            ratedobject.name = ratedobject_form["name"].value()
            ratedobject.description = ratedobject_form["description"].value()
            ratedobject.save()
            url = reverse('ratedobject_show', kwargs={'ratedmodel_name' : ratedmodel_name, 'ratedobject_name' : ratedobject_name,
                'ratedobject_id' : ratedobject_id})
            return HttpResponseRedirect(url)
        print(ratedobject_form.errors)
    else:
        ratedobject_form = RatedObjectForm(instance = ratedobject)
    current_user = request.user
    return render_to_response('ratedobject_edit.html', {"current_user": current_user, "ratedobject_form": ratedobject_form, "ratedobject": ratedobject}, context)

def is_url_valid(ratedmodel, ratedobject_name, ratedobject):
    if strip_non_alphanum(ratedobject.name) != ratedobject_name or ratedobject.ratedmodel_id != ratedmodel.id:
        return False
    return True