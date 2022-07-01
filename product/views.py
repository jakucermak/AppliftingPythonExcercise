from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .const import ProductError as Err


@api_view(['POST'])
def register_product(request):

    product_desc = ""
    product_name = ""

    if len(request.data) < 1:
            content_msg = {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': Err.prod_no_field_err.value
            }
            return Response(content_msg, status=status.HTTP_400_BAD_REQUEST)

    if not 'product_name' in request.data:
        content_msg = {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': Err.prod_name_err.value
            }
        return Response(content_msg, status=status.HTTP_400_BAD_REQUEST)
    else:
        product_name = request.data['product_name']

    if not 'product_desc' in request.data:
        content_msg = {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': Err.prod_desc_err.value
            }
        return Response(content_msg, status=status.HTTP_400_BAD_REQUEST)
    else:
        product_desc = request.data['product_desc']

    new_product = Product(product_name=product_name, product_description=product_desc)
    new_product.save()

    return Response(status=status.HTTP_201_CREATED)
