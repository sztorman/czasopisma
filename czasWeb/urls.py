# -*- coding: utf-8 -*-

from django.conf.urls import *

urlpatterns = patterns(
    '',
    (r'^$', 'czasWeb.views.about'),
    (r'^about/$', 'czasWeb.views.about'),
    (r'^resource/$', 'czasWeb.views.resource'),
    (r'^search/$', 'czasWeb.views.searchAdv'),
    (r'^search/results/$', 'czasWeb.views.searchResults'),
    (r'^listMagazines/(\d+)/(\d+)/$', 'czasWeb.views.listMagazines'),
    (r'^browse/$', 'czasWeb.views.browse'),
    (r'^single/(\d+)/$', 'czasWeb.views.single'),
    (r'^thumbnails/(\d+)/(\d+)/$', 'czasWeb.views.showThumbnails'),
    (r'^zoom/(\d+)/(\d+)/$', 'czasWeb.views.zoom'),
    (r'^double/(\d+)/(\d+)/$', 'czasWeb.views.double'),
    (r'^download/$', 'czasWeb.views.download'),
)