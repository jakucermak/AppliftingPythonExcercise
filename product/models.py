from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=100, blank=False, null=False)
    product_description = models.CharField(max_length=250, blank=True, null=True)

