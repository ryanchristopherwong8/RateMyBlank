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
def create(request, ratedModelName, ratedModelId, ratedObjectName, ratedObjectId):
  context = RequestContext(request)
  if request.method == "POST":
    dt = datetime.now()
    df = DateFormat(dt)
    current_user = request.user
    userProfile = UserProfile.objects.get(user = current_user)
    review = Review.objects.create(reviewer_id = userProfile.id, rated_object_id = ratedObjectId, created_at = df.format('Y-m-d'))

    scores = request.POST.getlist('score')
    attributes = request.POST.getlist('attribute_id')
    _addScoreModels(scores, attributes, review.id)

    url = reverse('ratedobjectshow', kwargs={'ratedModelName' : ratedModelName, 'ratedModelId' : str(ratedmodel.id),
    'ratedObjectName' : ratedObjectName, 'ratedObjectId' : ratedObjectId})
    return HttpResponseRedirect(url)

  else:
    current_user = request.user
    attributes = Attribute.objects.filter(rated_model = ratedModelId)
    return render_to_response('submit_review.html', {"current_user": current_user, "attributes" : attributes}, context)

def _addScoreModels(scores, attributes, review):
  index = 0
  for score in scores:
    Score.objects.create(review_id = review, grade = int(score), attribute_id = attributes[index])
    index += 1