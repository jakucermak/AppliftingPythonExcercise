
from django.core.management.base import BaseCommand
from faker import Faker
from product.models import Product



class Command(BaseCommand):
    help = "Provide Info"

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        for _ in range(15):
            uuid = fake.unique.uuid4(cast_to=None)
            prod_name = fake.unique.pystr()
            prod_desc = fake.sentence(nb_words=10)

            Product.objects.create(uuid=uuid,product_name=prod_name,product_description=prod_desc)
        