from django.db import models

class product(models.Model):
    name = models.BinaryField()
    price = models.IntegerField()
    details = models.BinaryField()


class order(models.Model):
    product = models.ForeignKey('products.product', on_delete=models.PROTECT)
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
            cost += o.product.price * o.number
        return cost

    #add a product to cart
    def add_product(self, ID):
        #check if this id is availble
        if not product.objects.filter(id=ID):
            return False
        has_related_order = False
        for o in self.order_set.all():
            if o.product.id == ID:
                has_related_order = True
                break
        if has_related_order:
            o.number += 1
            o.save()
            return True
        else:
            new_order = order(product=product.objects.get(id=ID), cart=self)
            new_order.save()
            return True

    #remove a product from cart
    def remove_product(self, ID):
        #check if this id is availble
        if not product.objects.filter(id=ID):
            return False
        has_related_order = False
        for o in self.order_set.all():
            if o.product.id == ID:
                has_related_order = True
                break
        if has_related_order:
            o.number -= 1
            if o.number > 0:
                o.save()
            else:
                o.delete()
            return True
        return False
        
            



