
from urllib import response
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Product
from .const import ProductError as Err

class ProductsCreateTests(APITestCase):
    def test_for_successfully_created_product(self):

        data = {
        'product_name': "motorovka",
        'product_desc': "ta co přeřízne cokoliv"
        }

        url = reverse('register')
        
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().product_name, 'motorovka')

    def test_for_not_provided_prod_name(self):

        data = {
            'product_desc': "secret thing"
        }

        url = reverse('register')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': Err.prod_name_err.value
            })

    def test_for_not_provided_prod_desc(self):

        data = {
            'product_name': 'magic wand'
        }

        url = reverse('register')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'code': status.HTTP_400_BAD_REQUEST,
            'message': Err.prod_desc_err.value
        })

    def test_for_no_field_provided(self):
        
        url = reverse('register')

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'code': status.HTTP_400_BAD_REQUEST,
            'message': Err.prod_no_field_err.value
        })






