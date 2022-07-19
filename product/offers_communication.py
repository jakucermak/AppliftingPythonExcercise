
import requests
from rest_framework.views import Response

from product_ms.settings import BASE_URL as base_url



class OffersMicroserviceCommunicationLayer():

    def __init__(self):
        self.__session = requests.Session()
        token = self.__session.post(f'{base_url}/auth/').json()['access_token']
        self.__session.headers.update({'Bearer' : token}) 


    def register_product(self, product):

        data_for_ms = {
            'id': product.id,
            'name': product.product_name,
            'description': product.product_description
        }
        response = self.__session.post(f'{base_url}/products/register',data_for_ms)
        return Response(data=response.json(),status=response.status_code)

