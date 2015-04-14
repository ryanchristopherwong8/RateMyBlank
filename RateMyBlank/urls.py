from django.conf.urls import patterns, include, url
from django.contrib import admin
from src.views import views
from src.views import userview
from src.views import ratedmodelview
from src.views import ratedobjectview

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RateMyBlank.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', ratedmodelview.index, name='index'),
    url(r'^ratedmodel/submit/$', ratedmodelview.submit, name='ratedmodelsubmit'),
    url(r'^(?P<ratedModelName>[-\w]+)/(?P<ratedModelId>[-\w]+)/$', ratedmodelview.show, name='ratedmodelshow'),
    url(r'^(?P<ratedModelName>[-\w]+)/(?P<ratedModelId>[-\w]+)/(?P<ratedObjectName>[-\w]+)/(?P<ratedObjectId>[-\w]+)/', ratedobjectview.show, name='ratedobjectshow'),
    url(r'^(?P<ratedModelName>[-\w]+)/(?P<ratedModelId>[-\w]+)/create/$', ratedobjectview.create, name='ratedobjectcreate'),
    url(r'^signup/$', userview.register, name='register'),
    url(r'^login/$', userview.user_login, name='login'),
    url(r'^logout/$', userview.user_logout, name='logout'),
)