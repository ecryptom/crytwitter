from django.urls import path
from .views import *

urlpatterns = [
    path('tweets', tweets, name='tweets'),
    path('curr_tweets/<str:curr_name>', curr_tweets, name='curr_tweets'),
    path('tweet', tweet, name='tweet'),
    path('retweet/<int:ID>', retweet, name='retweet'),

    #########  APIs   #######3
    path('last_twits', last_twits, name='last_twits'),
    path('like_tweet/<int:ID>', like_tweet, name='like_tweet'),
]