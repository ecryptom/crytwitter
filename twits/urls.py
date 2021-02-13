from django.urls import path
from .views import *

urlpatterns = [
    path('tweets', tweets, name='tweets'),
    path('last_twits', last_twits, name='last_twits'),
    path('ajax', ajax)
]