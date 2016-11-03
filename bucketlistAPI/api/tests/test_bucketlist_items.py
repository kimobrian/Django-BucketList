from api.models import BucketListItem, BucketList
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class BucketListItemsTests(APITestCase):
    """Tests for bucketlist items"""

    def setUp(self):
        """Register test user"""
        self.client.post('/auth/register/',
                         {'username': 'testuser',
                          'password': 'testpass',
                          'email': 'test@email.com'
                          },
                         format='json')
        """Login user/Client"""
        response = self.client.post('/auth/login/',
                                    {'username': 'testuser',
                                     'password': 'testpass'},
                                    format='json')
        self.token = response.data['auth_token']
        self.client.force_authenticate(token=self.token)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Test user
        user = User()
        user.username = 'testuser2'
        user.email = 'test2@email.com'
        user.password = 'pass1234'
        user.save()

        # Test bucketlist
        bucketlist = BucketList()
        bucketlist.name = 'First Bucketlist'
        bucketlist.created_by = user
        bucketlist.save()

        # Test Bucketlist item
        bucketlist_item = BucketListItem()
        bucketlist_item.item_name = 'Bucketlist Item'
        bucketlist_item.bucketlist = bucketlist
        bucketlist_item.save()

    def test_adding_items_to_someones_bucketlist(self):
        """Test trying to add a bucketlist to someone else's bucketlist"""
        response = self.client.post(
            '/bucketlists/1/items/', data={"item_name": "Bucketlist Item"},
            format='json')
        self.assertEqual(response.data, {"detail": "Not found."})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_adding_items_to_bucketlist_that_does_not_exist(self):
        """Test addition of items to bucketlist that does not exist"""
        response = self.client.post(
            '/bucketlists/456/items/', data={"item_name": "Bucketlist Item"},
            format='json')
        self.assertEqual(response.data, {"detail": "Not found."})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_updating_item_on_someone_elses_bucketlist(self):
        """Test trying to update items to someone elses bucketlist"""
        response = self.client.put(
            '/bucketlists/1/items/1/', data={"item_name": "Bucketlist Item"},
            format='json')
        self.assertEqual(response.data, {"detail": "Not found."})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_deleting_of_bucket_list_tem_that_does_not_exist(self):
        """Test for the deletion of a bucketlist item that does not exist"""
        response = self.client.get('/bucketlists/34/items/74/')
        self.assertEqual(response.data, {"detail": "Not found."})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_succesful_deletion_of_bucketlist_item(self):
        """Test that a bucketlist item is deleted successfully"""
        pass
