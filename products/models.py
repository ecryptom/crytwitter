from django.db import models
from utils.date_convertor import gregorian_to_shamsi
from django.utils import timezone

class product(models.Model):
    name = models.CharField(max_length=60, verbose_name='نام محصول')
    price = models.IntegerField(verbose_name='قیمت')
    off = models.IntegerField(default=0, verbose_name='تخفیف به درصد')
    details = models.TextField(default='', verbose_name='توضیحات کلی')
    details2 = models.TextField(default='', verbose_name='بخش توضیحات')
    group = models.ForeignKey('products.product_group', on_delete=models.CASCADE, null=True)
    File = models.FileField(upload_to='product_files', null=True, blank=True, verbose_name='فایل')
    properties = models.TextField(default='کیفیت:مناسب', verbose_name='ویژگی ها')
    status = models.CharField(max_length=10, choices=(('موجود', 'موجود'), ('ناموجود', 'ناموجود')), default=('موجود', 'موجود'), verbose_name='وضعیت')
    tags = models.CharField(max_length=50 ,default='crypto;BTC;miner', verbose_name='تگ‌ها(با ; جدا شوند)')  #split tags with ";"
    image1 = models.FileField(upload_to='products', verbose_name='تصویر اول')
    image2 = models.FileField(upload_to='products', null=True,blank=True, verbose_name='تصویر دوم')
    image3 = models.FileField(upload_to='products', null=True,blank=True, verbose_name='تصویر سوم')
    image4 = models.FileField(upload_to='products', null=True,blank=True, verbose_name='تصویر چهارم')
    image5 = models.FileField(upload_to='products', null=True,blank=True, verbose_name='تصویر پنجم')
    image6 = models.FileField(upload_to='products', null=True,blank=True, verbose_name='تصویر ششم')
    def net_price(self):
        return int(self.price * (100 - self.off) * 0.01)
    def split_tags(self):
        return self.tags.split(';')
    def split_properties(self):
        properties = []
        for p in self.properties.replace('\r','').split('\n'):
            try:
                p = p.split(':')
                properties.append({'key':p[0], 'value':p[1]})
            except:
                pass
        return properties
    def is_available(self):
        return self.status == 'موجود'
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'محصولات'


class product_group(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name   
    class Meta:
        verbose_name_plural = 'دسته بندی محصولات'

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
            if o.product.is_available():
                cost += o.product.price * o.number * (100-o.product.off) * 0.01
        return int(cost)

    #return number of product in cart
    def product_counter(self):
        count = 0
        for o in self.order_set.all():
            count += o.number
        return count

    #add a product to cart
    def add_product(self, ID):
        #check if this id is availble
        Product = product.objects.filter(id=ID)
        if not Product:
            return 0
        #check if product is available
        if not Product[0].is_available():
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
        Product = product.objects.filter(id=ID)
        if not Product:
            return 0
        #check if product is available
        if not Product[0].is_available():
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




