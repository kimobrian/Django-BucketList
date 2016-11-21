from api.models import BucketList
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class BucketListsTests(APITestCase):
    """Tests for API Endpoints"""

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

    def test_forbidden_access_to_bucket_list(self):
        """Test that user can only access a bucketlist they created"""
        user = User()
        user.username = 'testuser3'
        user.email = 'test3@email.com'
        user.password = 'pass12345'
        user.save()

        bucketlist = BucketList()
        bucketlist.name = 'First Bucketlist'
        bucketlist.created_by = user
        bucketlist.save()

        response = self.client.get('/bucketlists/1/')
        self.assertEqual(
            response.data, {"detail":
                            "You do not have permission"
                            " to perform this action."})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_of_bucketlist_with_no_data(self):
        """Test for creation of bucketlist without providing data"""
        response = self.client.post('/bucketlists/', format='json')
        self.assertEqual(response.data, {"name": ["This field is required."]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creation_of_empty_bucketlist(self):
        """Test for creation of bucketlist without providing data"""
        response = self.client.post(
            '/bucketlists/', data={"name": ""}, format='json')
        self.assertEqual(
            response.data, {"name": ["This field may not be blank."]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_successful_creation_of_bucketlist(self):
        """Test for successful creation of bucketlist"""
        response = self.client.post(
            '/bucketlists/', data={"name": "bucketlist name"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('bucketlist name', str(response.data))

    def test_creation_of_duplicate_bucketlist(self):
        """Test creation of duplicate bucketlist"""
        self.client.post(
            '/bucketlists/', data={"name": "bucketlist name"}, format='json')
        response = self.client.post(
            '/bucketlists/', data={"name": "bucketlist name"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {"name": ["Bucketlist name Exists"]})

    def test_update_of_bucketlist(self):
        """Test for update of bucketlist"""
        # Create bucketlist
        create_response = self.client.post('/bucketlists/',
                                           {'name': 'New Bucketlist'},
                                           format='json')
        bucketlist_id = str(create_response.data['id'])
        # Update created bucketlist
        response = self.client.put(
            '/bucketlists/' + bucketlist_id +
            '/', {'name': 'Editting first Bucketlist'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Editting first Bucketlist', str(response.data))

    def test_bucketlist_delete(self):
        """Test for deletion of bucketlist"""
        response = self.client.post('/bucketlists/',
                                    {'name': 'New Bucketlist'},
                                    format='json')
        bucketlist_id = str(response.data['id'])
        response = self.client.delete('/bucketlists/' + bucketlist_id + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deletion_of_non_existent_bucketlist(self):
        """Test deletion of a bucketlist that does not exist"""
        delete_response = self.client.delete('/bucketlists/20/')
        self.assertEqual(delete_response.status_code,
                         status.HTTP_404_NOT_FOUND)
