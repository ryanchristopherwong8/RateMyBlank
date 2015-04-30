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
from django.forms.formsets import formset_factory

class RatedModelForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    class Meta:
        model = RatedModel
        fields = ('name', 'description')

class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ('name', )

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
    attributes = ratedmodel.attribute_set.all()
    return render(request, 'ratedmodel.html', {"ratedobjects": ratedobjects, "current_user": current_user, "ratedmodel": ratedmodel, "attributes": attributes})

#create new models
def create(request):
    context = RequestContext(request)
    AttributeFormSet = formset_factory(AttributeForm)
    if request.method == "POST":
        rated_model_form = RatedModelForm(request.POST)
        attribute_formset = AttributeFormSet(request.POST, request.FILES)
        if rated_model_form.is_valid():
            if attribute_formset.is_valid():
                ratedmodel = rated_model_form.save(commit=True)
                for attribute_form in attribute_formset.forms:
                    attribute = attribute_form.save(commit=False)
                    attribute.rated_model_id = ratedmodel.id
                    attribute.save()
                url = reverse('ratedmodelshow', kwargs={'ratedModelName' : ratedmodel.name.replace(" ",""), 'ratedModelId' : str(ratedmodel.id)})
                return HttpResponseRedirect(url)
        print(rated_model_form.errors)
    else:
        rated_model_form = RatedModelForm()
    current_user = request.user
    return render_to_response('submit_ratedmodel.html', {"current_user": current_user, "rated_model_form": rated_model_form, 'attribute_formset': AttributeFormSet()}, context)

