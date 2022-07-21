
import uuid
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .offers_communication import OffersMicroserviceCommunicationLayer
from .constants import error
from .models import Product


class ProductsCreateTests(APITestCase):

    def test_for_successfully_created_product(self):

        off_comm_layer = OffersMicroserviceCommunicationLayer()
        off_comm_layer.auth()

        data = {
        'description': "ta co přeřízne cokoliv",
        'name': "motorovka",
        }

        url = reverse('product')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'motorovka')

    def test_for_not_provided_prod_name(self):

        data = {
            'description': "secret thing"
        }

        url = reverse('product')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': error.PROD_NAME_ERR
            })

    def test_for_not_provided_prod_desc(self):

        data = {
            'name': 'magic wand'
        }

        url = reverse('product')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'code': status.HTTP_400_BAD_REQUEST,
            'message': error.PROD_DESC_ERR
        })

    def test_for_no_field_provided(self):

        url = reverse('product')

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'code': status.HTTP_400_BAD_REQUEST,
            'message': error.PROD_INFO_ERR
        })

class DeleteProductTests(APITestCase):

    def test_delete_valid_product(self):

        faker = Faker()

        uuid = faker.unique.uuid4(cast_to=None)
        name = faker.unique.pystr()
        desc = faker.sentence(nb_words=10)

        Product.objects.create(uuid=uuid,name=name,description=desc)

        data = { 'uuid': str(uuid)}
        url = reverse('product')
        response = self.client.delete(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, { 'message' : 'deleted'})

    def test_delete_non_provided_uuid(self):
        data = {

        }
        url = reverse('product')
        response = self.client.delete(url,data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'message': error.PROD_UUID_ERR})

    def test_delete_non_existing_product(self):
        data = {
            'uuid' : str(uuid.uuid4())
        }
        url = reverse('product')
        response = self.client.delete(url,data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'message' : error.PROD_PRODNOTFOUND_ERR})



