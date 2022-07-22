
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .utils import get_last_used_token
from .constants import error
from .models import Product, Offer
from .serializers import ProductSerializer
from .offers_communication import get_offers, OffersMicroserviceCommunicationLayer as OffersCommLayer, get_offers_for_product

class ProductView(APIView):

    off_comm_lay = OffersCommLayer()

    def post (self, request):

        if not request.data:
            return Response(data={'code': status.HTTP_400_BAD_REQUEST,
            'message': error.PROD_INFO_ERR},status=status.HTTP_400_BAD_REQUEST)

        if 'name' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = 
            {'code': status.HTTP_400_BAD_REQUEST, 'message' : error.PROD_NAME_ERR})
        if 'description' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data =
             {'code': status.HTTP_400_BAD_REQUEST, 'message' : error.PROD_DESC_ERR})

        new_product = Product.objects.create(name=request.data['name'],description=request.data['description'])

        register_to_offers = self.off_comm_lay.register_product(new_product, get_last_used_token())

        return Response(register_to_offers.data,register_to_offers.status_code)


    def delete (self, request):

        if not 'uuid' in request.data:
            return Response({'message': error.PROD_UUID_ERR },status.HTTP_400_BAD_REQUEST)

        try:
            Product.objects.get(uuid=request.data['uuid']).delete()
        except ObjectDoesNotExist:
            return Response({'message': error.PROD_PRODNOTFOUND_ERR}, status.HTTP_400_BAD_REQUEST)

        return Response({'message':'deleted'},status=status.HTTP_200_OK)

    def patch(self, request):

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


@api_view(['GET'])
def offers(request):
    token = get_last_used_token()
    response = get_offers(token)
    return Response(data=response.data, status=response.status_code)

@api_view(['POST'])
def get_auth_token(request):
    authenticate = OffersCommLayer().auth()
    return Response(data=authenticate.data, status=authenticate.status_code)

@api_view(['GET'])
def update_offers(request,pk):

    try:
        product = Product.objects.get(id=pk)
    except ObjectDoesNotExist:
        Response(data={'message' : error.PROD_PRODNOTFOUND_ERR},status=status.HTTP_400_BAD_REQUEST)

    token = get_last_used_token()
    offers_from_ms = get_offers_for_product(product.id, token)
    if offers_from_ms == 200:
        Offer().update_or_create_offer(product=product, product_offers=offers_from_ms)

    return Response(data=offers_from_ms.data, status=offers_from_ms.status_code)