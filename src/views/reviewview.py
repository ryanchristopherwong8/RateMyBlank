from django.shortcuts import render
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from src.models.ratedmodel import RatedModel
from src.models.ratedobject import RatedObject
from src.models.review import Review
from src.models.attribute import Attribute
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from src.models.userprofile import UserProfile
from src.models.score import Score
import pdb

#create new models
def create(request, ratedmodel_name, ratedmodel_id, ratedobject_name, ratedobject_id):
    context = RequestContext(request)
    if request.method == "POST":
        dt = datetime.now()
        df = DateFormat(dt)
        current_user = request.user
        userprofile = UserProfile.objects.get(user=current_user)
        review = Review.objects.create(user_id = userprofile.id, ratedobject_id = ratedobject_id, created_at = df.format('Y-m-d'))
        scores = request.POST.getlist('score')
        attributes = request.POST.getlist('attribute_id')
        _add_score_models(scores, attributes, review.id)
        url = reverse('ratedobjects_show', kwargs={'ratedmodel_name' : ratedmodel_name, 'ratedmodel_id' : str(ratedmodel.id),
            'ratedobject_name' : ratedobject_name, 'ratedobject_id' : ratedobject_id})
        return HttpResponseRedirect(url)
    else:
        current_user = request.user
        attributes = Attribute.objects.filter(ratedmodel = ratedmodel_id)
        return render_to_response('review_create.html', {"current_user": current_user, "attributes" : attributes}, context)

def _add_score_models(scores, attributes, review):
    index = 0
    for score in scores:
        Score.objects.create(review_id = review, grade = int(score), attribute_id = attributes[index])
        index += 1