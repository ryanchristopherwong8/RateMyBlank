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
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory, BaseFormSet
from django.db.models import Avg

class RatedModelForm(forms.ModelForm):
    name = forms.CharField(error_messages={'required': 'This field is required!'})
    class Meta:
        model = RatedModel
        fields = ('name', 'description')

class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ('name', )

class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            self.forms[0].empty_permitted = False

#Show all
def index(request):
    current_user = request.user
    ratedmodels = RatedModel.objects.order_by("-created_at")
    return render(request, 'index.html', {"ratedmodels": ratedmodels, "current_user": current_user})

#Show one
def show(request, ratedmodel_name, ratedmodel_id):
    current_user = request.user
    ratedmodel = RatedModel.objects.get(pk=ratedmodel_id)
    ratedobjects = RatedObject.objects.filter(ratedmodel_id=ratedmodel_id).order_by("-created_at").annotate(overall_grade = Avg('review__score__grade'))
    attributes = ratedmodel.attribute_set.all()
    return render(request, 'ratedmodel_show.html', {"ratedobjects": ratedobjects, "current_user": current_user, "ratedmodel": ratedmodel, "attributes": attributes})

#create new models
def create(request):
    if not request.user.is_authenticated():
        return redirect("login")
    context = RequestContext(request)
    AttributeFormSet = formset_factory(AttributeForm, formset=RequiredFormSet)
    if request.method == "POST":
        ratedmodel_form = RatedModelForm(request.POST)
        attribute_formset = AttributeFormSet(request.POST, request.FILES)
        if ratedmodel_form.is_valid():
            if attribute_formset.is_valid():
                ratedmodel = ratedmodel_form.save(commit=True)
                for attribute_form in attribute_formset.forms:
                    if attribute_form["name"].value():
                        attribute = attribute_form.save(commit=False)
                        attribute.ratedmodel_id = ratedmodel.id
                        attribute.save()
                url = reverse('ratedmodel_show', kwargs={'ratedmodel_name' : ratedmodel.name.replace(" ",""), 'ratedmodel_id' : str(ratedmodel.id)})
                return HttpResponseRedirect(url)
        print(ratedmodel_form.errors)
    else:
        ratedmodel_form = RatedModelForm()
    current_user = request.user
    return render_to_response('ratedmodel_create.html', {"current_user": current_user, "ratedmodel_form": ratedmodel_form, 'attribute_formset': AttributeFormSet()}, context)

