
from rest_framework import serializers
from .models import Offer, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'uuid', 'name', 'description']

class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ['id', 'price', 'items_in_stock', 'product_id']
