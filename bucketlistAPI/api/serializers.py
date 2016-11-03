from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import BucketList, BucketListItem


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    email = serializers.EmailField(max_length=100, required=True)
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        pass


class BucketListItemSerializer(serializers.ModelSerializer):
    """Serializer for BucketListItem model"""
    item_name = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = BucketListItem
        fields = ('id', 'item_name', 'date_created', 'date_modified', 'done')


class BucketListSerializer(serializers.ModelSerializer):
    """Serializer for BucketList model"""
    name = serializers.CharField(max_length=100, required=True)
    bucketlist_items = BucketListItemSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.id')

    class Meta:
        model = BucketList
        fields = ('id', 'name', 'created_by',
                  'date_created', 'date_modified', 'bucketlist_items')
