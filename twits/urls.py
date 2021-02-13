from django.urls import path
from .views import *

urlpatterns = [
    path('tweets', tweets, name='tweets'),
    path('tweet', tweet, name='tweet'),

    #########  APIs   #######3
    path('last_twits', last_twits, name='last_twits'),
    path('like_tweet/<int:ID>', like_tweet, name='like_tweet'),
]