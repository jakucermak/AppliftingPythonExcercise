from django.urls import path
from .views import get_product, offers, update_offers


urlpatterns = [
    path('<int:pk>', get_product),
    path('offers/', offers),
    path('offers/<int:pk>/update/', update_offers)
    ]