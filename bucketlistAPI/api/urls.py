from api import views
from django.conf.urls import url
from api.views import (BucketListView, SingleBucketListView,
                       BucketListItemsCreationView,
                       BucketListItemOperationsView)


urlpatterns = [
    url(r'^$', views.index),
    url(r'^bucketlists/$', BucketListView.as_view()),
    url(r'^bucketlists/(?P<id>\d+)/$', SingleBucketListView.as_view()),
    url(r'^bucketlists/(?P<id>\d+)/items/$',
        BucketListItemsCreationView.as_view()),
    url(r'^bucketlists/(?P<id>\d+)/items/(?P<pk>\d+)/$',
        BucketListItemOperationsView.as_view()),
]
