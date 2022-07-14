
import requests
from product_ms.settings import BASE_URL as base_url

def register_product(data):

    
    response = requests.post(f'{base_url}/products/register',data)

    return response