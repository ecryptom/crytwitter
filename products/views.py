from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *
from utils.date_convertor import gregorian_to_shamsi
from django.utils import timezone
from django.http import JsonResponse
from zeep import Client
import os


#payment variables
MERCHANT = os.getenv('MERCHANT')
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
CallbackURL = os.getenv('BASE_URL') + '/product/payment_verify'


def product_page(req, ID):
    if req.method == 'GET':
        return render(req, 'product.html', {'product': product.objects.get(id=ID)})

def products_page(req):
    groups = product_group.objects.all()
    return render(req, 'list-products.html', {'product_groups':groups})

@login_required(login_url='login')
def cart_page(req):
    Cart = cart.objects.filter(user=req.user).filter(paid=False)
    return render(req, 'panel-shopping-cart.html', {
        'cart': Cart[0] if (Cart and Cart[0].order_set.all()) else None, 
        'paid_carts': cart.objects.filter(user=req.user).filter(paid=True)
        })


@login_required(login_url='login')
def add_product_to_cart(req, ID):
    Cart = cart.objects.filter(user=req.user).filter(paid=False)
    if not Cart:
        Cart = cart(user=req.user)
        Cart.save()
    else:
        Cart = Cart[0]
    Cart.add_product(ID)
    return redirect('cart')


@login_required(login_url='login')
def comment(req, ID):
    Text = req.POST.get('text')
    if not Text:
        return redirect('product', ID=ID)
    Product = product.objects.get(id=ID)
    User = req.user
    Date = gregorian_to_shamsi(timezone.now())
    comment = product_comment(product=Product, user=User, text=Text, shamsi_date=Date)
    comment.save()
    return redirect('product', ID=ID)

@csrf_exempt
@login_required(login_url='login')
def reply_comment(req, ID):
    Text = req.POST.get('text')
    Date = gregorian_to_shamsi(timezone.now())
    Comment = product_comment.objects.get(id=ID)
    if not Text:
        return redirect('product', ID=Comment.product.id)
    Reply_comment = product_comment(product=Comment.product, user=req.user, shamsi_date=Date, text=Text, reply_to=Comment)
    Reply_comment.save()
    return redirect('product', ID=Comment.product.id)




@login_required(login_url='login')
def payment_request(req, ID):
    Cart = cart.objects.get(id=ID)
    if Cart.cost() == 0:
        return redirect('cart')
    #check request user and cart status
    if req.user != Cart.user or Cart.paid:
        return redirect('cart')
    result = client.service.PaymentRequest(MERCHANT, Cart.cost(), f'user_id:{req.user.id}, username:{req.user.username}', req.user.email, req.user.phone, CallbackURL)
    if result.Status == 100:
        Cart.Authority = str(result.Authority)
        Cart.save()
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))
        
 
@login_required(login_url='login')
def payment_verify(req):
    Cart = cart.objects.get(Authority=req.GET.get('Authority'))
    if not Cart:
        return redirect('cart')
    if not req.user.phone == Cart.user.phone:
        return redirect('cart')
    result = client.service.PaymentVerification(MERCHANT, req.GET.get('Authority'), Cart.cost())
    if result.Status == 100:
        Cart.paid = True
        Cart.status = 'pending'
        Cart.RefID = str(result.RefID)
        Cart.save()
        return redirect('cart')
    else:
        return redirect('cart')


#############   APIs  ############
@csrf_exempt
@login_required
def add_product(req, ID):
    Cart = cart.objects.filter(user=req.user).filter(paid=False)
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
    Cart = cart.objects.filter(user=req.user).filter(paid=False)
    if not Cart:
        return JsonResponse({'status':'failed'})
    remaining_number = Cart[0].remove_product(ID)
    return JsonResponse({'status':'success', 'number': remaining_number, 'cost':Cart[0].cost()})