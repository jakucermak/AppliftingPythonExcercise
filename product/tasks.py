from celery import Celery, shared_task
from django.db import transaction


from product.models import Offer, Product
from .utils import get_last_used_token
from .offers_communication import get_offers_for_product

app = Celery()

@shared_task
def update_offer_prices():

    products = Product.objects.all()

    token = get_last_used_token()

    with transaction.atomic():
        for product in products:
            offers_response = get_offers_for_product(product.id,token)

            if offers_response.status_code == 200:
                Offer().update_or_create_offer(product=product,product_offers=offers_response.data)
