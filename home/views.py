from django.shortcuts import render
from .models import currency
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

def home(req):
    return render(req, 'index.html', {'top_curs': currency.objects.filter(id__lt=11)})

def cryptomarket(req):
    return render(req, 'cryptomarket.html')



########  APIs    ########33
@csrf_exempt
@login_required(login_url='login')
def get_all_currencies(req):
    return JsonResponse([{
        'name': cur.name,
        'symbol' : cur.symbol,
        'persian_name' : cur.persian_name.decode(),
        'image_url' : cur.image_url
    } for cur in currency.objects.all()], safe=False)

