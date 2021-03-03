from django.db import models
from utils.date_convertor import gregorian_to_shamsi
from django.utils import timezone

class product(models.Model):
    name = models.CharField(max_length=25, verbose_name='نام محصول')
    price = models.IntegerField(verbose_name='قیمت')
    off = models.IntegerField(default=0, verbose_name='تخفیف به درصد')
    details = models.TextField(default='', verbose_name='توضیحات')
    details2 = models.TextField(default='', verbose_name='توضیحات پایین')
    tags = models.CharField(max_length=50 ,default='crypto;BTC;miner', verbose_name='تگ‌ها(با ; جدا شوند)')  #split tags with ";"
    image1 = models.FileField(upload_to='products', null=True,blank=True, verbose_name='تصویر اول')
    image2 = models.FileField(upload_to='products', null=True,blank=True, verbose_name='تصویر دوم')
    image3 = models.FileField(upload_to='products', null=True,blank=True, verbose_name='تصویر سوم')
    def net_price(self):
        return self.price * (100 - self.off) * 0.01
    def split_tags(self):
        return self.tags.split(';')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'محصولات'


class order(models.Model):
    product = models.ForeignKey('products.product', on_delete=models.CASCADE, verbose_name='محصول')
    cart = models.ForeignKey('products.cart', on_delete=models.CASCADE, verbose_name='سبد خرید')
    number = models.IntegerField(default=1, verbose_name='تعداد')


class cart(models.Model):
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    RefID = models.CharField(max_length=30, null=True, blank=True)
    Authority = models.CharField(max_length=45, null=True, blank=True)
    status = models.CharField(max_length=10, choices=(('payment', 'payment'), ('pending', 'pending'), ('done', 'done')), default='payment')

    class Meta:
        verbose_name_plural = 'سفارشات'

    #return the cost of cart
    def cost(self):
        cost = 0
        for o in self.order_set.all():
            cost += o.product.price * o.number * (100-o.product.off) * 0.01
        return cost

    #add a product to cart
    def add_product(self, ID):
        #check if this id is availble
        if not product.objects.filter(id=ID):
            return 0
        has_related_order = False
        for o in self.order_set.all():
            if o.product.id == ID:
                has_related_order = True
                break
        if has_related_order:
            o.number += 1
            o.save()
            return o.number
        else:
            new_order = order(product=product.objects.get(id=ID), cart=self, number=1)
            new_order.save()
            return 1

    #remove a product from cart
    def remove_product(self, ID):
        #check if this id is availble
        if not product.objects.filter(id=ID):
            return 0
        has_related_order = False
        for o in self.order_set.all():
            if o.product.id == ID:
                has_related_order = True
                break
        if has_related_order:
            o.number -= 1
            if o.number > 0:
                o.save()
                return o.number
            else:
                o.delete()
                return 0
        return 0

    def cart_info(self):
        info = ''
        for o in self.order_set.all():
            info += f'''
                محصول:  {o.product.name}
                تعداد:  {o.number}
                -----------------------\n
            '''
        info += f'\n قیمت کل:  {self.cost()}'
        return info
        
            
class product_comment(models.Model):
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    shamsi_date = models.CharField(max_length=11)
    text = models.TextField()
    reply_to = models.ForeignKey('products.product_comment', related_name='replies_in', on_delete=models.CASCADE, null=True)




