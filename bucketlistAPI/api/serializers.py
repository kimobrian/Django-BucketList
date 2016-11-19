from api.models import BucketList, BucketListItem
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)

    def validate_email(self, email):
        if not email:
            raise serializers.ValidationError("Email Address is required")
        check_email = User.objects.filter(email__iexact=email)
        if check_email:
            raise serializers.ValidationError("Email Address Already in Use")
        return email

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class BucketListItemSerializer(serializers.ModelSerializer):
    """Serializer for BucketListItem model"""
    item_name = serializers.CharField(max_length=100, required=True)

    def validate(self, data):
        """Bucket list item name can not be empty."""
        if data['item_name'] == '':
            raise serializers.ValidationError('Item name is required')
        return data

    class Meta:
        model = BucketListItem
        fields = ('id', 'item_name', 'date_created', 'date_modified', 'done')


class BucketListSerializer(serializers.ModelSerializer):
    """Serializer for BucketList model"""
    name = serializers.CharField(max_length=100, required=True)
    bucketlist_items = BucketListItemSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.id')

    def validate(self, data):
        """Bucketlist name can not be empty"""
        print(data)
        if not data["name"]:
            raise serializers.ValidationError('Bucketlist name is required.')
        return data

    def validate_name(self, name):
        user = self.context['request'].user
        check_bucketlist = BucketList.objects.filter(name__iexact=name,
                                                     created_by=user)
        if check_bucketlist:
            raise serializers.ValidationError("Bucketlist name Exists")
        return name

    class Meta:
        model = BucketList
        fields = ('id', 'name', 'created_by',
                  'date_created', 'date_modified', 'bucketlist_items')
