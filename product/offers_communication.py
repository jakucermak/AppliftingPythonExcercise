from collections import namedtuple
import requests
from django.db import transaction

from product_ms.settings import BASE_URL as base_url
from .models import Offer, Product, Token


class OffersMicroserviceCommunicationLayer():

    def __init__(self):
        self.__session = requests.Session()

    def auth(self):
        response = self.__session.post(f'{base_url}/auth/')
        token = Token.objects.create(value=response.json()['access_token'])

        ResponseFromMS = namedtuple('ResponseFromMS',['status_code', 'data'])

        return ResponseFromMS(status_code=response.status_code, data={'access-token': token.value})

    def register_product(self, product, token):

        self.__session.headers.update({'Bearer' : token})

        data_for_ms = {
            'id': product.id,
            'name': product.name,
            'description': product.description
        }
        response = self.__session.post(f'{base_url}/products/register', data_for_ms)

        ResponseFromMS = namedtuple('ResponseFromMS',['status_code', 'data'])

        return ResponseFromMS(response.status_code, response.json())


def get_offers_for_product(pk, token):

    ResponseFromMS = namedtuple('ResponseFromMS',['status_code', 'data'])

    session = requests.Session()
    session.headers.update({'Bearer' : token})

    response = session.get(f'{base_url}/products/{pk}/offers')

    return ResponseFromMS(response.status_code,response.json())

def get_offers(token):

    products = Product.objects.all()
    ResponseFromMS = namedtuple('ResponseFromMS',['status_code', 'data'])

    
    with transaction.atomic(): 
        for product in products:
            offers_response = get_offers_for_product(product.id,token)

            if offers_response.status_code != 200:
                return offers_response
            for offer in offers_response.data:
                Offer.objects.create(id=offer['id'], price=offer['price'], items_in_stock=offer['items_in_stock'], product=product)
    
    return ResponseFromMS(data={'message' : 'ok'},status_code=200)

