from api import views
from django.conf.urls import url
from api.views import (BucketListView, SingleBucketListView,
                       BucketListItemsCreationView, HomePageView,
                       BucketListItemOperationsView)


urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard/$', views.dashboard),
    url(r'^docs/$', views.schema_view),
    url(r'^bucketlists/$', BucketListView.as_view()),
    url(r'^bucketlists/(?P<id>\d+)/$', SingleBucketListView.as_view()),
    url(r'^bucketlists/(?P<id>\d+)/items/$',
        BucketListItemsCreationView.as_view()),
    url(r'^bucketlists/(?P<id>\d+)/items/(?P<pk>\d+)/$',
        BucketListItemOperationsView.as_view()),
]
