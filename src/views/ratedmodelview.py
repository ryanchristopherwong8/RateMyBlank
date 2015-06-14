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
from src.helpers.application_helper import strip_non_alphanum

class RatedModelForm(forms.ModelForm):
    name = forms.CharField(error_messages={'required': 'This field is required!'})
    class Meta:
        model = RatedModel
        fields = ('name', 'description')
    def clean(self):
        name = self.cleaned_data['name']
        stripped_name = strip_non_alphanum(name)
        model_check = RatedModel.objects.filter(name_key=stripped_name)
        if model_check:
            raise forms.ValidationError({'name': ["A page already exists with a similar name. Please choose another name.",]})
        return self.cleaned_data

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
    ratedmodels = RatedModel.objects.filter(is_deleted=False).order_by("-created_at")
    return render(request, 'index.html', {"ratedmodels": ratedmodels, "current_user": current_user})

#Show one
def show(request, ratedmodel_name_key):
    current_user = request.user
    ratedmodel = RatedModel.objects.get(name_key=ratedmodel_name_key, is_deleted=False)
    ratedobjects = RatedObject.objects.filter(ratedmodel_id=ratedmodel.id).order_by("-created_at").annotate(overall_grade = Avg('review__score__grade'))
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
                ratedmodel = ratedmodel_form.save(commit=False)
                ratedmodel.name_key = strip_non_alphanum(ratedmodel.name)
                ratedmodel.creator_id = request.user.userprofile.id
                ratedmodel.save()
                tag_title = ratedmodel.name.lower()
                ratedmodel.tags.add(tag_title, *tag_title.split(' '))
                for attribute_form in attribute_formset.forms:
                    if attribute_form["name"].value():
                        attribute = attribute_form.save(commit=False)
                        attribute.ratedmodel = ratedmodel
                        attribute.save()
                url = reverse('ratedmodel_show', kwargs={'ratedmodel_name_key' :ratedmodel.name_key})
                return HttpResponseRedirect(url)
        print(ratedmodel_form.errors)
    else:
        ratedmodel_form = RatedModelForm()
    current_user = request.user
    return render_to_response('ratedmodel_create.html', {"current_user": current_user, "ratedmodel_form": ratedmodel_form, 'attribute_formset': AttributeFormSet()}, context)

def edit(request, ratedmodel_name_key):
    if not request.user.is_authenticated():
        return redirect("login")
    ratedmodel = RatedModel.objects.get(pk=ratedmodel_name_key, is_deleted=False)
    if request.user.userprofile.id != ratedmodel.creator_id:
        url = reverse('ratedmodel_show', kwargs={'ratedmodel_name_key' : ratedmodel.name_key})
        return HttpResponseRedirect(url)
    context = RequestContext(request)
    if request.method == "POST":
        ratedmodel_form = RatedModelForm(request.POST)
        if ratedmodel_form.is_valid():
            ratedmodel.name = ratedmodel_form["name"].value()
            ratedmodel.description = ratedmodel_form["description"].value()
            ratedmodel.save()
            url = reverse('ratedmodel_show', kwargs={'ratedmodel_name_key' : ratedmodel.name_key})
            return HttpResponseRedirect(url)
        print(ratedmodel_form.errors)
    else:
        ratedmodel_form = RatedModelForm(instance = ratedmodel)
    current_user = request.user
    return render_to_response('ratedmodel_edit.html', {"ratedmodel": ratedmodel, "current_user": current_user, "ratedmodel_form": ratedmodel_form}, context)

def delete(request, ratedmodel_name_key):
    if not request.user.is_authenticated():
        return redirect("login")
    ratedmodel = RatedModel.objects.get(pk=ratedmodel_name_key)
    if request.user.userprofile.id != ratedmodel.creator_id:
        url = reverse('ratedmodel_show', kwargs={'ratedmodel_name_key' : ratedmodel.name_key})
        return HttpResponseRedirect(url)
    if request.method == "POST":
        ratedmodel.is_deleted = True
        ratedmodel.save()
        return redirect("index")
    context = RequestContext(request)
    current_user = request.user
    ratedmodel_form = RatedModelForm()
    return render_to_response('ratedmodel_delete.html', {"ratedmodel": ratedmodel, "current_user": current_user}, context)
