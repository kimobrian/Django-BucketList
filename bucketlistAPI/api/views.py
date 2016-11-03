from api.custom_permission import IsOwner
from django.shortcuts import render, get_object_or_404
from api.models import BucketList, BucketListItem
from rest_framework_swagger.views import get_swagger_view
from rest_framework.generics import (
    ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from api.pagination import BucketListPagination
from api.serializers import (BucketListItemSerializer,
                             BucketListSerializer)
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

schema_view = get_swagger_view(title='Bucketlist API')


def index(request):
    return render(request, 'index.html', {})


def dashboard(request):
    return render(request, 'main.html', {})


def current_bucketlist(obj):
    """Get bucketlist from ID in url"""
    bucketlist_id = obj.kwargs.get('id')
    return get_object_or_404(
        BucketList,
        id=int(bucketlist_id),
        created_by=obj.request.user
    )


class HomePageView(APIView):
    # permission_classes = (IsAuthenticated, IsOwner)
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        return Response(template_name='main.html')


class BucketListView(ListCreateAPIView):
    """
    Returns list of bucketlists(GET request)
    Creates new bucket list (POST request)

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


class SingleBucketListView(RetrieveUpdateDestroyAPIView):
    """
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
    pagination_class = BucketListPagination
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


class BucketListItemOperationsView(RetrieveUpdateDestroyAPIView):

    """
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
        item_id = self.kwargs.get('id')  # Bucketlist Item ID
        queryset = BucketListItem.objects.filter(
            bucketlist=bucketlist).filter(id=item_id)
        return queryset
