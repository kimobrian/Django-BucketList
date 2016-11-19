from rest_framework.pagination import PageNumberPagination


class BucketListPagination(PageNumberPagination):
    page_size = 5
