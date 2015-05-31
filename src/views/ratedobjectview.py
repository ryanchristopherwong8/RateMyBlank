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

class RatedObjectForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    class Meta:
        model = RatedObject
        fields = ('name', 'description')

def show(request, ratedmodel_name, ratedmodel_id, ratedobject_name, ratedobject_id):
    current_user = request.user
    ratedobject = RatedObject.objects.get(pk = ratedobject_id)
    reviews = ratedobject.review_set.annotate(avg_grade = Avg('score__grade'))
    attributes = ratedobject.ratedmodel.attribute_set.filter(score__review__ratedobject_id = ratedobject_id).annotate(avg_grade = Avg('score__grade'))
    overall_grade = list(ratedobject.review_set.aggregate(Avg('score__grade')).values())[0]
    return render(request, 'ratedobject_show.html', {"ratedobject": ratedobject, "ratedmodel": ratedobject.ratedmodel, "reviews": reviews, "attributes": attributes,
        "overall_grade": overall_grade, "current_user": current_user})

def create(request, ratedmodel_name, ratedmodel_id):
    if not request.user.is_authenticated():
        return redirect("login")
    context = RequestContext(request)
    try:
        ratedmodel = RatedModel.objects.get(pk = ratedmodel_id)
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