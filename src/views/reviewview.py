from django.shortcuts import render
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from src.models.ratedmodel import RatedModel
from src.models.ratedobject import RatedObject
from src.models.review import Review
from src.models.userprofile import UserProfile
from src.models.score import Score
from src.models.attribute import Attribute
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django import forms
from django.forms.formsets import formset_factory

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('description', )

class ScoreForm(forms.ModelForm):
    attribute_id = forms.IntegerField()
    attribute_name = forms.CharField(max_length=200, required=False)
    class Meta:
        model = Score
        fields = ('grade',)

#create new models
def create(request, ratedmodel_name, ratedmodel_id, ratedobject_name, ratedobject_id):
    if not request.user.is_authenticated():
        return redirect("login")
    context = RequestContext(request)
    ScoreFormSet = formset_factory(ScoreForm, extra=0)
    if request.method == "POST":
        userprofile = request.user.userprofile
        review_form = ReviewForm(request.POST)
        score_formset = ScoreFormSet(request.POST, request.FILES)
        if review_form.is_valid():
            if score_formset.is_valid():
                review = review_form.save(commit=False)
                review.userprofile_id = userprofile.id
                review.ratedobject_id = ratedobject_id
                review.save()
                for score_form in score_formset.forms:
                    score = score_form.save(commit=False)
                    score.attribute_id = score_form["attribute_id"].value()
                    score.review_id = review.id
                    score.save()
                url = reverse('review_show', kwargs={'ratedmodel_name' : ratedmodel_name, 'ratedmodel_id' : ratedmodel_id,
                    'ratedobject_name' : ratedobject_name, 'ratedobject_id' : ratedobject_id, 'review_id' : review.id})
                return HttpResponseRedirect(url)
        print(score_formset.errors)
    else:
        review_form = ReviewForm()
    current_user = request.user
    attributes = Attribute.objects.filter(ratedmodel = ratedmodel_id)
    score_formset = ScoreFormSet(initial=[{'attribute_id': attribute.id, 'attribute_name': attribute.name} for attribute in attributes])
    return render_to_response("review_create.html", {"current_user": current_user, "review_form": review_form, 'score_formset': score_formset}, context)

def show(request, ratedmodel_name, ratedmodel_id, ratedobject_name, ratedobject_id, review_id):
    current_user = request.user
    review = Review.objects.get(pk = review_id)
    attributes = Attribute.objects.filter(ratedmodel = ratedmodel_id)
    scores = Score.objects.filter(review = review_id)
    return render(request, "review_show.html", {"review": review, "current_user" : current_user, "scores" : scores})