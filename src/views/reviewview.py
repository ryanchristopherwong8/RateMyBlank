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
import pdb

class ReviewForm(forms.ModelForm):
    attribute_id = forms.IntegerField()
    attribute_name = forms.CharField(max_length=200, required=False)
    review_id = forms.IntegerField(required = False)
    is_deleted = forms.BooleanField(initial = False, required = False)
    class Meta:
        model = Review
        fields = ('description', 'score', )
        widgets = {
            'description': forms.Textarea(attrs={'class': 'review-description-input'}),
            'score': forms.NumberInput(attrs={'class': 'review-score-input'}),
        }

#create and edit reviews
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
                if review_form["review_id"].value():
                    review_id = review_form["review_id"].value()
                    old_review = Review.objects.get(pk = review_id)
                    if old_review.ratedobject_id == ratedobject.id:
                        if review_form["is_deleted"] and review_form["is_deleted"].value() == True:
                            old_review.is_deleted = True
                        else:
                            old_review.description = review_form["description"].value()
                            old_review.score = review_form["score"].value()
                        old_review.save()
                else:
                    review = review_form.save(commit=False)
                    review.userprofile_id = userprofile.id
                    review.ratedobject_id = ratedobject_id
                    attribute = Attribute.objects.get(pk=review_form["attribute_id"].value())
                    if attribute.ratedmodel_id == ratedmodel.id:
                        review.attribute_id = attribute.id
                    else:
                        continue
                    review.save()
        url = reverse('ratedobject_show', kwargs={'ratedmodel_name_key' : ratedmodel.name_key, 'ratedobject_name' : ratedobject_name,
            'ratedobject_id' : ratedobject_id})
        return HttpResponseRedirect(url)
    current_user = request.user
    attributes = Attribute.objects.filter(ratedmodel = ratedmodel.id)
    user_reviews = Review.objects.filter(userprofile_id = current_user.userprofile.id, ratedobject_id = ratedobject_id, is_deleted=False)
    review_formset = ReviewFormSet(initial=[{'attribute_id': attribute.id, 'attribute_name': attribute.name,
        'description' : _getReviewDescription(user_reviews, attribute.id), 'score' : _getReviewScore(user_reviews, attribute.id),
        'review_id': _getReviewId(user_reviews, attribute.id)} for attribute in attributes])
    return render_to_response("review_create.html", {"current_user": current_user, "review_formset": review_formset, 'ratedobject': ratedobject}, context)

# TODO: what should this be?
def show(request, ratedmodel_name, ratedmodel_id, ratedobject_name, ratedobject_id, review_id):
    current_user = request.user
    review = Review.objects.get(pk = review_id)
    attributes = Attribute.objects.filter(ratedmodel = ratedmodel_id)
    scores = Score.objects.filter(review = review_id)
    return render(request, "review_show.html", {"review": review, "current_user" : current_user, "scores" : scores})

def _getReviewDescription(reviews, attribute_id):
    try:
        description = reviews.get(attribute_id = attribute_id).description
    except:
        description = None
    return description

def _getReviewScore(reviews, attribute_id):
    try:
        score = reviews.get(attribute_id = attribute_id).score
    except:
        score = None
    return score

def _getReviewId(reviews, attribute_id):
    try:
        review_id = reviews.get(attribute_id = attribute_id).id
    except:
        review_id = None
    return review_id