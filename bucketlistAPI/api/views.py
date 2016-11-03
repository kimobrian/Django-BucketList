from api.custom_permission import IsOwner
from api.models import BucketList
from rest_framework_swagger.views import get_swagger_view
from rest_framework.generics import (
    ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from api.pagination import BucketListPagination
from api.serializers import (BucketListItemSerializer,
                             BucketListSerializer)


schema_view = get_swagger_view(title='Bucketlist API')


def index(request):
    pass


def dashboard(request):
    pass


def current_bucketlist(obj):
    """Get bucketlist from ID in url"""
    pass


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
        pass

    def get_queryset(self):
        """Return list of bucketlists"""
        pass


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
        pass


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
        pass
