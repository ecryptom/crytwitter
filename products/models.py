from django.db import models
from utils.date_convertor import gregorian_to_shamsi
from django.utils import timezone

class product(models.Model):
    name = models.BinaryField()
    price = models.IntegerField()
    off = models.IntegerField(default=0)
    details = models.BinaryField()
    tags = models.BinaryField(default=b'')  #split tags with ";"
    image1 = models.FileField(upload_to='products', null=True)
    image2 = models.FileField(upload_to='products', null=True)
    image3 = models.FileField(upload_to='products', null=True)
    def net_price(self):
        return self.price * (100 - self.off) * 0.01
    def split_tags(self):
        return self.tags.decode().split(';')


class order(models.Model):
    product = models.ForeignKey('products.product', on_delete=models.CASCADE)
    cart = models.ForeignKey('products.cart', on_delete=models.CASCADE)
    number = models.IntegerField(default=1)


class cart(models.Model):
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    RefID = models.CharField(max_length=30, null=True, blank=True)
    Authority = models.CharField(max_length=45, null=True, blank=True)

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
        
            
class product_comment(models.Model):
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    shamsi_date = models.CharField(max_length=11)
    text = models.BinaryField()
    reply_to = models.ForeignKey('products.product_comment', related_name='replies_in', on_delete=models.CASCADE, null=True)




