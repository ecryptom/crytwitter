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
    path('list_currencies/<int:page>', list_currencies, name='list_currencies'),
    path('about_us', about_us, name='about_us'),


    ######  APIs  #######
    path('get_all_currencies', get_all_currencies, name='get_all_currencies'),
    path('get_top_currencies_info/<int:count>', get_top_currencies_info, name='get_top_currencies_info'),
    path('get_currencies_info/<int:page>', get_currencies_info, name='get_currencies_info'),
    path('get_currency_info/<str:symbol>', get_currency_info, name='get_currency_info'),
]