from .views import auth
from django.urls import path


urlpatterns = [
    path('auth/', auth, name = 'auth' )
]