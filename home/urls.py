from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('cryptomarket', cryptomarket, name='cryptomarket'),
    path('article/<int:ID>', article_page, name='article'),
    path('articles', articles, name='articles'),
    path('article_comment/<int:ID>', article_comment_view, name='article_comment'),
    path('reply_article_comment/<int:ID>', reply_article_comment_view, name='reply_article_comment'),
    path('index_search', index_search, name='index_search'),


    ######  APIs  #######
    path('get_all_currencies', get_all_currencies, name='get_all_currencies'),
    path('get_first_10_currency_info', get_first_10_currency_info, name='get_first_10_currency_info'),
    path('get_search_objects', get_search_objects, name='get_search_objects'),
]