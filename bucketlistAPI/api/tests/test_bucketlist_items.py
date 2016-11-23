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

    def test_deleting_of_bucket_list_item_that_does_not_exist(self):
        """Test for the deletion of a bucketlist item that does not exist"""
        response = self.client.get('/bucketlists/34/items/74/')
        self.assertEqual(response.data, {"detail": "Not found."})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_successful_creation_of_bucketlist_item(self):
        """Test that a bucketlist item is created successfully"""
        response = self.client.post('/bucketlists/',
                                    data={"name": "Bucketlist name"})
        bucketlist_id = response.data.get('id')
        response = self.client.post(
            '/bucketlists/' + str(bucketlist_id) + '/items/',
            data={"item_name": "Item in bucketlist"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creation_of_duplicate_bucketlist_item(self):
        """Test for creation of duplicate bucketlist items"""
        response = self.client.post('/bucketlists/',
                                    data={"name": "Bucketlist name"})
        bucketlist_id = response.data.get('id')
        self.client.post(
            '/bucketlists/' + str(bucketlist_id) + '/items/',
            data={"item_name": "Item in bucketlist"})
        response = self.client.post(
            '/bucketlists/' + str(bucketlist_id) + '/items/',
            data={"item_name": "Item in bucketlist"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {"item_name": ["Item name already exists"]})

    def test_successful_deletion_of_bucketlist_item(self):
        """Test that a bucketlist item is deleted succesfully"""
        response = self.client.post('/bucketlists/',
                                    data={"name": "Bucketlist name"})
        bucketlist_id = response.data.get('id')
        bucketlist_item = self.client.post(
            '/bucketlists/' + str(bucketlist_id) + '/items/',
            data={"item_name": "Item in bucketlist"})
        item_id = bucketlist_item.data.get('id')
        response = self.client.delete(
            '/bucketlists/' + str(
                bucketlist_id) + '/items/' + str(item_id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_successful_update_of_bucketlist_item(self):
        """Test that an item is updated successfully"""
        response = self.client.post('/bucketlists/',
                                    data={"name": "Bucketlist name"})
        bucketlist_id = response.data.get('id')
        bucketlist_item = self.client.post(
            '/bucketlists/' + str(bucketlist_id) + '/items/',
            data={"item_name": "Item in bucketlist"})
        item_id = bucketlist_item.data.get('id')
        response = self.client.put(
            '/bucketlists/' + str(bucketlist_id) + '/items/' + str(
                item_id) + '/', data={"item_name": "Updated item name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Updated item name", str(response.data))
