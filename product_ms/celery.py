

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_ms.settings')

app = Celery('product_ms')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'update_offers' : {
        'task' : 'product.tasks.update_offer_prices',
        'schedule': 60,
    }
}

app.autodiscover_tasks()
