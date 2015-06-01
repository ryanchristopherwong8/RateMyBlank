from django.conf.urls import patterns, include, url
from django.contrib import admin
from src.views import views
from src.views import userview
from src.views import ratedmodelview
from src.views import ratedobjectview
from src.views import reviewview
from src.views import tagview

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RateMyBlank.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Home
    url(r'^$', ratedmodelview.index, name='index'),

    # Tags
    url(r'^search/$', tagview.create, name='tagview_create'),
    url(r'^search=(?P<tag_name>[\w\+\s]*)/?$', tagview.index, name='tagview_index'),

    # Rated Model
    url(r'^ratedmodel/create/$', ratedmodelview.create, name='ratedmodel_create'),
    url(r'^(?P<ratedmodel_name>[-\w]+)/(?P<ratedmodel_id>[-\w]+)/$', ratedmodelview.show, name='ratedmodel_show'),
    url(r'^(?P<ratedmodel_name>[-\w]+)/(?P<ratedmodel_id>[-\w]+)/edit$', ratedmodelview.edit, name='ratedmodel_edit'),

    # Rated Object
    url(r'^(?P<ratedmodel_name>[-\w]+)/(?P<ratedmodel_id>[-\w]+)/(?P<ratedobject_name>[-\w]+)/(?P<ratedobject_id>[-\w]+)/$', ratedobjectview.show, name='ratedobject_show'),
    url(r'^(?P<ratedmodel_name>[-\w]+)/(?P<ratedmodel_id>[-\w]+)/create/$', ratedobjectview.create, name='ratedobject_create'),

    # Review
    url(r'^(?P<ratedmodel_name>[-\w]+)/(?P<ratedmodel_id>[-\w]+)/(?P<ratedobject_name>[-\w]+)/(?P<ratedobject_id>[-\w]+)/review/create/$', reviewview.create, name = 'review_create'),
    url(r'^(?P<ratedmodel_name>[-\w]+)/(?P<ratedmodel_id>[-\w]+)/(?P<ratedobject_name>[-\w]+)/(?P<ratedobject_id>[-\w]+)/review/(?P<review_id>[-\w]+)/$', reviewview.show, name ='review_show'),

    #User
    url(r'^signup/$', userview.register, name='register'),
    url(r'^login/$', userview.user_login, name='login'),
    url(r'^logout/$', userview.user_logout, name='logout'),
)