from django.db import models
import uuid

class Product(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
    uuid = models.UUIDField(primary_key=False, editable=False, default=uuid.uuid4)
    product_name = models.CharField(max_length=100, blank=False, null=False)
    product_description = models.CharField(max_length=250, blank=True, null=True)

