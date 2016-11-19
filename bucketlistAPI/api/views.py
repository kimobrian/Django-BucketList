from api.custom_permission import IsOwner
from api.models import BucketList, BucketListItem
from api.pagination import BucketListPagination
from api.serializers import (BucketListItemSerializer,
                             BucketListSerializer)
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import (ListAPIView, UpdateAPIView,
                                     DestroyAPIView, CreateAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


def index(request):
    return render(request, 'index.html', {})


def current_bucketlist(obj):
    """Get bucketlist from ID in url"""
    bucketlist_id = obj.kwargs.get('id')
    return get_object_or_404(
        BucketList,
        id=int(bucketlist_id),
        created_by=obj.request.user
    )


class BucketListView(ListAPIView, CreateAPIView):
    """
    Creates a bucketlist(POST) and return bucketlists(GET)

    Method: GET
      Parameters:
          page  (optional)    default=1
      Header:
          AuthorizationToken  (required)
      Response: JSON

    Method: POST
      Parameters:
          name  (required)
      Header:
          AuthorizationToken  (required)
      Response: JSON
    """
    serializer_class = BucketListSerializer
    pagination_class = BucketListPagination
    permission_classes = (IsOwner, IsAuthenticated)

    def perform_create(self, serializer):
        """Create new bucketlist"""
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        """Return list of bucketlists"""
        queryset = BucketList.objects.filter(created_by=self.request.user)
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response([serializer.data])


class SingleBucketListView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    """
    Retrieves(GET) , Updates(PUT) and Deletes(DELETE) a bucketlist
    Return single bucketlist and its items(GET request)
    Update single bucketlist(PUT request)
    Delete Single Bucketlist(DELETE Request)

    Method: GET
      Header:
          AuthorizationToken  (required)
      Response: JSON

    Method: PUT
      Parameters:
          name  (required)
      Header:
          AuthorizationToken  (required)
      Response: JSON

    Method: DELETE
      Header:
          AuthorizationToken  (required)
      Response: JSON

    """
    queryset = BucketList.objects.all()
    serializer_class = BucketListSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    lookup_field = 'id'


class BucketListItemsCreationView(CreateAPIView):
    """
    Creates a new bucketlist item
    Method: POST
        Parameters:
            name (required)
        Header:
            AuthorizationToken (required)
        Response: JSON
    """
    serializer_class = BucketListItemSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        bucketlist = current_bucketlist(self)
        serializer.save(bucketlist=bucketlist)


class BucketListItemOperationsView(UpdateAPIView,
                                   DestroyAPIView, RetrieveAPIView):

    """
    Updates(PUT) and Deletes(DELETE) a bucketlist Item
    Update bucketlist Item(PUT)
    Delete bucketlist Item(DELETE)

    Method: PUT
      Parameters:
          task  (optional)
          done  (optional)
      Header:
          AccessToken  (required)
      Response: JSON

    Method: DELETE
      Header:
          AccessToken  (required)
      Response: JSON
    """
    serializer_class = BucketListItemSerializer
    permission_classes = (IsOwner, IsAuthenticated)

    def get_queryset(self):
        bucketlist = current_bucketlist(self)
        item_id = self.kwargs.get('pk')  # Bucketlist Item ID
        queryset = BucketListItem.objects.filter(
            bucketlist=bucketlist).filter(id=item_id)
        return queryset
