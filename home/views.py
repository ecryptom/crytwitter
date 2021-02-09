from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from utils.date_convertor import gregorian_to_shamsi

def home(req):
    return render(req, 'index.html', {'top_curs': currency.objects.all()[:10], 'dollor_rate':dollor.objects.get().rate})

def cryptomarket(req):
    return render(req, 'cryptomarket.html')

def article_page(req, ID):
    Article = article.objects.get(id=ID)
    return render(req, 'article.html', {'article':Article, 'article_chunks':Article.article_chunk_set.order_by('number')})


@login_required(login_url='login')
def article_comment_view(req, ID):
    Text = req.POST.get('text')
    Article = article.objects.get(id=ID)
    User = req.user
    Date = gregorian_to_shamsi(timezone.now())
    Comment = article_comment(article=Article, user=User, text=Text, shamsi_date=Date)
    Comment.save()
    return redirect('article', ID=ID)


@csrf_exempt
@login_required(login_url='login')
def reply_article_comment_view(req, ID):
    Text = req.POST.get('text')
    Date = gregorian_to_shamsi(timezone.now())
    Comment = article_comment.objects.get(id=ID)
    Reply_comment = article_comment(article=Comment.article, user=req.user, shamsi_date=Date, text=Text, reply_to=Comment)
    Reply_comment.save()
    return redirect('article', ID=Comment.article.id)




########  APIs    ########33
@csrf_exempt
@login_required(login_url='login')
def get_all_currencies(req):
    return JsonResponse([{
        'name': cur.name,
        'symbol' : cur.symbol,
        'persian_name' : cur.persian_name,
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


