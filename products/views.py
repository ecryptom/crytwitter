from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *
from utils.date_convertor import gregorian_to_shamsi
from django.utils import timezone
from django.http import JsonResponse

def product_page(req, ID):
    if req.method == 'GET':
        return render(req, 'product.html', {'product': product.objects.get(id=ID)})


@login_required(login_url='login')
def cart_page(req):
    Cart = cart.objects.filter(user=req.user)
    if Cart and Cart[0].order_set.all():
        return render(req, 'panel-shopping-cart.html', {'cart':Cart[0]})
    return render(req, 'panel-shopping-cart.html')


@login_required(login_url='login')
def add_product_to_cart(req, ID):
    Cart = cart.objects.filter(user=req.user)
    if not Cart:
        Cart = cart(user=req.user)
        Cart.save()
    else:
        Cart = Cart[0]
    Cart.add_product(ID)
    return redirect('cart')


@login_required(login_url='login')
def comment(req, ID):
    Text = req.POST.get('text').encode()
    Product = product.objects.get(id=ID)
    User = req.user
    Date = gregorian_to_shamsi(timezone.now())
    comment = product_comment(product=Product, user=User, text=Text, shamsi_date=Date)
    comment.save()
    return redirect('product', ID=ID)



#############   APIs  ############
@csrf_exempt
@login_required
def add_product(req, ID):
    Cart = cart.objects.filter(user=req.user)
    if not Cart:
        Cart = cart(user=req.user)
        Cart.save()
    else:
        Cart = Cart[0]
    remaining_number = Cart.add_product(ID)
    return JsonResponse({'status':'success', 'number': remaining_number, 'cost':Cart.cost()})

@csrf_exempt
@login_required
def remove_product(req, ID):
    Cart = cart.objects.filter(user=req.user)
    if not Cart:
        return JsonResponse({'status':'failed'})
    remaining_number = Cart[0].remove_product(ID)
    return JsonResponse({'status':'success', 'number': remaining_number, 'cost':Cart[0].cost()})