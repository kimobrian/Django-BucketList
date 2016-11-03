from api.models import BucketList, BucketListItem
from django.test import TestCase
from django.contrib.auth.models import User


class ModelTests(TestCase):
    """Tests for API models"""

    def setUp(self):
        user = User()
        user.username = 'testusername'
        user.email = 'test@email.com'
        user.password = 'pass123'
        user.save()

        bucketlist = BucketList()
        bucketlist.name = 'First Bucketlist'
        bucketlist.created_by = user
        bucketlist.save()

        bucketlist_item = BucketListItem()
        bucketlist_item.bucketlist = bucketlist
        bucketlist_item.save()

    def test_user_bucketlist_relationship(self):
        """
        Tests that when a user is deleted, all
        associated bucketlists are deleted too
        """
        bucketlist_count_before = BucketList.objects.count()
        User.objects.filter(id=1).delete()
        bucketlist_count_after = BucketList.objects.count()
        self.assertEqual(bucketlist_count_before - bucketlist_count_after, 1)

    def test_user_bucketlist_relationship2(self):
        """
        Tests that when a bucketlist is deleted, all
        associated bucketlist items are deleted too
        """
        bucketlist_items_count_before = BucketListItem.objects.count()
        BucketList.objects.filter(id=1).delete()
        bucketlist_items_count_after = BucketListItem.objects.count()
        self.assertEqual(bucketlist_items_count_before -
                         bucketlist_items_count_after, 1)
