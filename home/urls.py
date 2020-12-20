from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('<str:page>', page_resp)
]