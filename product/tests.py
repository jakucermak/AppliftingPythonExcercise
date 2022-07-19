
import uuid
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .constants import error
from .models import Product


class ProductsCreateTests(APITestCase):
    def test_for_successfully_created_product(self):

        data = {
        'product_name': "motorovka",
        'product_desc': "ta co přeřízne cokoliv"
        }

        url = reverse('product')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().product_name, 'motorovka')

    def test_for_not_provided_prod_name(self):

        data = {
            'product_desc': "secret thing"
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
            'product_name': 'magic wand'
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
        prod_name = faker.unique.pystr()
        prod_desc = faker.sentence(nb_words=10)

        Product.objects.create(uuid=uuid,product_name=prod_name,product_description=prod_desc)

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



