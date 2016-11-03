from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class BucketList(models.Model):
    '''BucketList model'''
    name = models.CharField(max_length=100, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bucketlists')

    class Meta:
        unique_together = ('created_by', 'name')


class BucketListItem(models.Model):
    """Bucketlist Item model"""
    item_name = models.CharField(
        max_length=100, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    bucketlist = models.ForeignKey(
        BucketList, on_delete=models.CASCADE, related_name='bucketlist_items')
    done = models.BooleanField(default=False)

    class Meta:
        unique_together = ('bucketlist', 'item_name')
