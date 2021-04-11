from django.contrib import admin
from .models import product, cart, product_group

@admin.register(product)
class ArticleAdmin_(admin.ModelAdmin):
    pass

@admin.register(cart)
class ArticleAdmin_(admin.ModelAdmin):
    verbose_name_plural = 'سفارشات'
    search_fields = ('status', 'paid')
    readonly_fields = ('cart_info', 'user_info')


@admin.register(product_group)
class productadmin(admin.ModelAdmin):
    verbose_name = 'سفارشات'