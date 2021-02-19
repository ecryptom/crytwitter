from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from utils.date_convertor import gregorian_to_shamsi

def home(req):
    return render(req, 'index.html', {
        'top_curs': currency.objects.all()[:10], 
        'dollor_rate':dollor.objects.get().rate,
        'questions': faq.objects.all(),
        'comments': index_comments.objects.all(),
        })

def cryptomarket(req):
    return render(req, 'cryptomarket.html')

def article_page(req, ID):
    Article = article.objects.get(id=ID)
    return render(req, 'article.html', {'article':Article})


@login_required(login_url='login')
def article_comment_view(req, ID):
    Text = req.POST.get('text')
    if not Text:
        return redirect('article', ID=ID)
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
    if not Text:
        return redirect('article', ID=Comment.article.id)
    Reply_comment = article_comment(article=Comment.article, user=req.user, shamsi_date=Date, text=Text, reply_to=Comment)
    Reply_comment.save()
    return redirect('article', ID=Comment.article.id)


def index_search(req):
    cur_name = req.POST['currency'].split('|')
    try:
        cur = currency.objects.get(name=cur_name[0])
    except:
        try:
            cur = currency.objects.get(name=cur_name[1])
        except:
            return redirect('home')
    return redirect('curr_tweets', cur.name)


def error_404(req, exception):
    return render(req, 'error_404.html')



########  APIs    ########33
@csrf_exempt
def get_all_currencies(req):
    return JsonResponse([{
        'name': cur.name,
        'symbol' : cur.symbol,
        'persian_name' : cur.persian_name,
        'image_url' : cur.image_url
    } for cur in currency.objects.all()], safe=False)


@csrf_exempt
def get_first_10_currency_info(req):
    return JsonResponse([{
        'symbol': cur.symbol,
        'price': cur.price,
        '1d_change': cur.daily_price_change_pct,
        '7d_change': cur.weekly_price_change_pct
    } for cur in currency.objects.all()[:10]], safe=False)


@csrf_exempt
def get_search_objects(req):
    #articles
    data = [{
        'subject': a.title,
        'image':'/static/img/article_icon.png',
        'type' : 'article',
    } for a in article.objects.all()]
    return JsonResponse(data, safe=False)