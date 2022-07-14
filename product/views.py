
import requests
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from product_ms.settings import BASE_URL as base_url
from . import error
from .models import Product
from .serializers import ProductSerializer
from .tasks import register_product


@api_view(['POST'])
def auth(request):
    return Response(requests.post(f'{base_url}/auth/'))

class ProductView(APIView):

    def post (self, request):

        product_desc = ""
        product_name = ""

        if len(request.data) < 1:
            content_msg = {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': error.PROD_INFO_ERR
            }
            return Response(content_msg, status=status.HTTP_400_BAD_REQUEST)
        #TODO: Remove string
        if not 'product_name' in request.data:
            content_msg = {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': error.PROD_NAME_ERR
                }
            return Response(content_msg, status=status.HTTP_400_BAD_REQUEST)

        product_name = request.data['product_name']
        #TODO: Same above
        if not 'product_desc' in request.data:
            content_msg = {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': error.PROD_DESC_ERR
                }
            return Response(content_msg, status=status.HTTP_400_BAD_REQUEST)

        product_desc = request.data['product_desc']

        new_product = Product(product_name=product_name, product_description=product_desc)
        new_product.save()

        data_for_ms = {
            'id': new_product.id,
            'name': new_product.product_name,
            'description': new_product.product_description
        }

        response_from_ms = register_product(data_for_ms)
        match response_from_ms.status_code:
            case 200:
                response = {
                'message': status.HTTP_201_CREATED,
                'id': new_product.id
            }

                return Response(response, status=status.HTTP_201_CREATED)
            case 400:
                return Response(response_from_ms.json(), status.HTTP_400_BAD_REQUEST)

            case 401: 
                return Response(response_from_ms.json(), status.HTTP_401_UNAUTHORIZED)


    def delete (self, request):

        #TODO: same above
        if not 'uuid' in request.data:
            return Response({'message': error.PROD_UUID_ERR },status.HTTP_400_BAD_REQUEST)

        try:
            Product.objects.get(uuid=request.data['uuid']).delete()
        except ObjectDoesNotExist:
            return Response({'message': error.PROD_PRODNOTFOUND_ERR}, status.HTTP_400_BAD_REQUEST)

        return Response({'message':'deleted'},status=status.HTTP_200_OK)

    def patch(self, request):
        #TODO: same above
        if not 'uuid' in request.data:
            return Response({'message' : error.PROD_UUID_ERR}, status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(uuid=request.data['uuid'])

        except ObjectDoesNotExist:
            return Response({'message' : error.PROD_UUID_ERR}, status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(product,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
