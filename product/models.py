from django.db import models
import uuid

class Product(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    uuid = models.UUIDField(primary_key=False, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=250, blank=True, null=True)

class Offer(models.Model):

    id = models.BigIntegerField(primary_key=True, db_column='id')
    price = models.BigIntegerField()
    items_in_stock = models.BigIntegerField(db_column='items_in_stock')
    product = models.ForeignKey(Product,on_delete = models.CASCADE, db_column='product_id')

    def update_or_create_offer(self, product, product_offers):

        for offer in product_offers:
            if not Offer.objects.filter(id=offer['id']):
                Offer.objects.create(id=offer['id'],price=offer['price'], items_in_stock=offer['items_in_stock'], product=product)
            Offer.objects.filter(id=offer['id']).update(price=offer['price'],items_in_stock=offer['items_in_stock'])


class Token(models.Model):

    class Owner(models.TextChoices):
        OFFERS_MS = 'offers_ms'
        PRODUCT_MS = 'product_ms'

    id = models.BigAutoField(auto_created=True,primary_key=True)
    value = models.CharField(blank=False,null=False,max_length=250)
    owner = models.CharField(max_length=10,choices=Owner.choices,default=Owner.PRODUCT_MS)
