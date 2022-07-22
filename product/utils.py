from product.models import Token

def get_last_used_token():
    token = Token.objects.last().value
    return token
