import json

from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from app import views
from app.models import Credentials, Workload, MountPoint, \
                       MigrationTarget, Migration
from app.serializers import CredentialsSerializer, WorkloadSerializer, \
                            MountPointSerializer, MigrationSerializer, \
                            MigrationTargetSerializer

class TestCredentials(APITestCase):
    def setUp(self):
        self.testCreds1 = Credentials.objects.create(
            user='test_user1',password='123',domain='testdomain'
        )
        self.testCreds2 = Credentials.objects.create(
            user='test_user2',password='321',domain='anotherdomain'
        )
        self.valid_create_payload = {
            'user': 'test_user3',
            'password': '123',
            'domain': 'somedomain'
        }
        self.invalid_create_payload = {
            'user': '',
            'pass': '000',
            'domain': 'justdomain'
        }
        self.valid_update_payload = {
            'user': 'test_user1',
            'password': '000',
            'domain': 'testdomain'
        }
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.view = views.CredentialsViewSet.as_view({'get': 'list'})
        self.uri = '/credentials/'
        
    def test_list(self):
        request = self.factory.get(self.uri)
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                          'Expected Response Code 200, received {0} instead.'
                          .format(response.status_code))
    
    def test_get_single_valid_creds(self):
        response = self.client.get(reverse('credentials-detail', kwargs={'pk': 1}))
        creds = Credentials.objects.get(pk=self.testCreds1.pk)
        serializer = CredentialsSerializer(creds)
        self.assertEqual(response.status_code, 200,
                          'Expected Response Code 200, received {0} instead.'
                          .format(response.status_code))
        self.assertEqual(response.data, serializer.data)

    def test_get_single_invalid_creds(self):
        response = self.client.get(reverse('credentials-detail', kwargs={'pk': 99}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_create_valid_creds(self):
        response = self.client.post(
            reverse('credentials-list'),
            data=json.dumps(self.valid_create_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_invalid_creds(self):
        response = self.client.post(
            reverse('credentials-list'),
            data=json.dumps(self.invalid_create_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_valid_creds(self):
        response = self.client.put(
            reverse('credentials-detail', kwargs={'pk': self.testCreds1.pk}),
            data=json.dumps(self.valid_update_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_valid_creds(self):
        response = self.client.delete(
            reverse('credentials-detail', kwargs={'pk': self.testCreds1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class TestWorkload(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.creds = Credentials.objects.create(
            user='test_user1', password='123', domain='testdomain'
        )
        self.mnt1 = MountPoint.objects.create(
            name='c', size=30000
        )
        self.mnt2 = MountPoint.objects.create(
            name='c', size=30000
        )
        '''
        self.workload = Workload.objects.create(
            ip='2.2.2.2', 
        )
        '''
        self.create_payload = {
            'ip': '1.1.1.1',
            'credentials': self.creds.pk,
            'mount_list': [ 1 ]
        }
        self.modify_payload_valid = {
            'ip': '1.1.1.1',
            'mount_list': [ 1, 2 ]
        }
        self.modify_payload_invalid = {
            'ip': '1.1.1.1',
            'credentials': 1,
            'mount_list': [ 1, 2 ]
        }
    def test_create_workload(self):
        response = self.client.post(
            reverse('workload-list'),
            data=json.dumps(self.create_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['ip'], Workload.objects.get(pk=1).ip)
        
    def test_modify_workload(self):
        self.client.post(
            reverse('workload-list'),
            data=json.dumps(self.create_payload),
            content_type='application/json')
        response = self.client.put(
            reverse('workload-detail', kwargs={'pk': 1} ),
            data=json.dumps(self.modify_payload_valid),
            content_type='application/json')
        print('resp:',response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
