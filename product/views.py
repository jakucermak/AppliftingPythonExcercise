from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from . import error
from .models import Product


@api_view(['POST'])
def register_product(request):

    product_desc = ""
    product_name = ""

    if len(request.data) < 1:
        content_msg = {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': error.PROD_INFO_ERR
        }
        return Response(content_msg, status=status.HTTP_400_BAD_REQUEST)

    if not 'product_name' in request.data:
        content_msg = {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': error.PROD_NAME_ERR
            }
        return Response(content_msg, status=status.HTTP_400_BAD_REQUEST)

    product_name = request.data['product_name']

    if not 'product_desc' in request.data:
        content_msg = {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': error.PROD_DESC_ERR
            }
        return Response(content_msg, status=status.HTTP_400_BAD_REQUEST)

    product_desc = request.data['product_desc']

    new_product = Product(product_name=product_name, product_description=product_desc)
    new_product.save()

    response = {
        'message': status.HTTP_201_CREATED,
        'id': new_product.uuid
    }
    return Response(response, status=status.HTTP_201_CREATED)

class Products(APIView):

    def delete (self, request):

        if not 'uuid' in request.data :
            return Response({'message': error.PROD_UUID_ERR },status.HTTP_400_BAD_REQUEST)
        
        try:
            Product.objects.get(uuid=request.data['uuid']).delete()
        except ObjectDoesNotExist:
            return Response({'message': error.PROD_PRODNOTFOUND_ERR}, status.HTTP_400_BAD_REQUEST)
        

        return Response({'message':'deleted'},status=status.HTTP_200_OK)
