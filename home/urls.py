from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('cryptomarket', cryptomarket, name='cryptomarket'),


    ######  APIs  #######
    path('get_all_currencies', get_all_currencies, name='get_all_currencies')
]