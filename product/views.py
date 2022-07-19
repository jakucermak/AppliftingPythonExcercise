

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .constants import error
from .models import Product
from .serializers import ProductSerializer
from .offers_communication import OffersMicroserviceCommunicationLayer as OffersCommLayer

class ProductView(APIView):

    off_comm_lay = OffersCommLayer()

    def post (self, request):

        product_desc, product_name = "",""

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

        return self.off_comm_lay.register_product(new_product)


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
            return Response({'message' : error.PROD_PRODNOTFOUND_ERR}, status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(product,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_product(request, pk):

    try:
        product = Product.objects.get(id=pk)

    except ObjectDoesNotExist:
        return Response({'message' : error.PROD_PRODNOTFOUND_ERR})

    serialized_product = ProductSerializer(product)
    return Response(status=status.HTTP_200_OK, data=serialized_product.data)
