from django.urls import path
from .views import *

urlpatterns = [
    path('<int:ID>', product_page, name='product'),
    path('all', products_page, name="products_page"),
    path('product_comment/<int:ID>', comment, name='product_comment'),
    path('reply_product_comment/<int:ID>', reply_comment, name='reply_product_comment'),
    path('cart', cart_page, name='cart'),
    path('add_product_to_cart/<int:ID>', add_product_to_cart, name='add_product_to_cart'),
    path('payment_request/<int:ID>', payment_request, name='payment_request'),
    path('payment_verify', payment_verify, name='payment_verify'),
    
    ### APIs ###
    path('add_product/<int:ID>', add_product, name='add_product'),
    path('remove_product/<int:ID>', remove_product, name='remove_product'),
    path('remove_order/<int:ID>', remove_order, name='remove_order'),
]