from django.shortcuts import render
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from src.models.ratedmodel import RatedModel
from src.models.ratedobject import RatedObject
from src.models.review import Review
from src.models.userprofile import UserProfile
from src.models.attribute import Attribute
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django import forms
from django.forms.formsets import formset_factory, BaseFormSet
from src.helpers.application_helper import strip_non_alphanum

class ReviewForm(forms.ModelForm):
    attribute_id = forms.IntegerField()
    attribute_name = forms.CharField(max_length=200, required=False)
    class Meta:
        model = Review
        fields = ('description', 'score', )
        widgets = {
            'description': forms.TextInput(attrs={'class': 'review-description-input'}),
            'score': forms.NumberInput(attrs={'class': 'review-score-input'}),
        }

#create new models
def create(request, ratedmodel_name_key, ratedobject_name, ratedobject_id):
    if not request.user.is_authenticated():
        return redirect("login")
    context = RequestContext(request)
    ratedobject = RatedObject.objects.get(pk=ratedobject_id)
    ratedmodel = RatedModel.objects.get(name_key=ratedmodel_name_key)
    if ratedobject_name != strip_non_alphanum(ratedobject.name) or ratedobject.ratedmodel_id != ratedmodel.id:
        return HttpResponse('<h1>Page was not found</h1>')
    ReviewFormSet = formset_factory(ReviewForm, extra=0)
    if request.method == "POST":
        userprofile = request.user.userprofile
        review_formset = ReviewFormSet(request.POST, request.FILES)
        for review_form in review_formset.forms:
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.userprofile_id = userprofile.id
                review.ratedobject_id = ratedobject_id
                attribute = Attribute.objects.get(pk=review_form["attribute_id"].value())
                if attribute.ratedmodel_id == ratedmodel.id:
                    review.attribute_id = attribute.id
                else:
                    break
                review.save()
        url = reverse('ratedobject_show', kwargs={'ratedmodel_name_key' : ratedmodel.name_key, 'ratedobject_name' : ratedobject_name,
            'ratedobject_id' : ratedobject_id})
        return HttpResponseRedirect(url)
    attributes = Attribute.objects.filter(ratedmodel = ratedmodel.id)
    review_formset = ReviewFormSet(initial=[{'attribute_id': attribute.id, 'attribute_name': attribute.name} for attribute in attributes])
    current_user = request.user
    return render_to_response("review_create.html", {"current_user": current_user, "review_formset": review_formset, 'ratedobject': ratedobject}, context)

def show(request, ratedmodel_name, ratedmodel_id, ratedobject_name, ratedobject_id, review_id):
    current_user = request.user
    review = Review.objects.get(pk = review_id)
    attributes = Attribute.objects.filter(ratedmodel = ratedmodel_id)
    scores = Score.objects.filter(review = review_id)
    return render(request, "review_show.html", {"review": review, "current_user" : current_user, "scores" : scores})