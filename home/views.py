from django.shortcuts import render
from .models import currency, dollor
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

def home(req):
    return render(req, 'index.html', {'top_curs': currency.objects.all()[:10], 'dollor_rate':dollor.objects.get().rate})

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


@csrf_exempt
@login_required(login_url='login')
def get_first_10_currency_info(req):
    return JsonResponse([{
        'symbol': cur.symbol,
        'price': cur.price,
        '1d_change': cur.daily_price_change_pct,
        '7d_change': cur.weekly_price_change_pct
    } for cur in currency.objects.all()[:10]], safe=False)


