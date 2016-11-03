from api.models import BucketList, BucketListItem
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """User can only operate on a bucketlist/items they own"""

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, BucketListItem):
            return obj.bucketlist.created_by == request.user
        elif isinstance(obj, BucketList):
            return obj.created_by == request.user
