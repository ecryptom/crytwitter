from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from utils.date_convertor import gregorian_to_shamsi
from twits.models import twit
from accounts.models import user


#count of currencies in on page of list_currencies
page_size = 40
#id of first currency
first_currency_id = currency.objects.first().id


#get a string and return cur if exist
def which_currency(str):
    cur_name = str.split('|')
    try:
        cur = currency.objects.get(name=cur_name[0])
    except:
        try:
            cur = currency.objects.get(symbol=cur_name[0])
        except:
            try:
                cur = currency.objects.get(name=cur_name[1])
            except:
                return None
    return cur


def home(req):
    return render(req, 'index.html', {
        'top_curs': currency.objects.order_by('-market_cap')[:12], 
        'articles': article.objects.order_by('-id'),
        'dollor_rate':dollor.objects.get().rate,
        'questions': faq.objects.all(),
        'comments': index_comments.objects.all(),
        'twits_count': twit.objects.count(),
        'users_count': user.objects.filter(verified_phone=True).count()
        })

def cryptomarket(req):
    return render(req, 'cryptomarket.html')

def article_page(req, ID):
    Article = article.objects.get(id=ID)
    Article.views_count += 1
    Article.save()
    return render(req, 'article.html', {'article':Article})

def articles(req):
    return render(req, 'list-articles.html', {'articles':article.objects.order_by('-id')})


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
    cur = which_currency(req.GET['currency'])
    if not cur:
        return redirect('home')
    return redirect('curr_tweets', cur.name)

def list_currencies(req, page):
    up_bound = first_currency_id + page_size * page
    currencies = currency.objects.filter(id__lt=up_bound).filter(id__gte=up_bound-page_size)
    symbols = ','.join([cur.symbol for cur in currencies])
    return render(req, 'list-cryptocurrency.html', {
        'currencies':currencies, 
        'symbols':symbols,
        'dollor_rate':dollor.objects.get().rate,
        'page':page,
        })


def error_404(req, exception):
    return render(req, 'error_404.html')
def error_500(req, *args, **argv):
    return render(req, 'error_500.html')



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
def get_top_currencies_info(req, count):
    return JsonResponse([{
        'symbol': cur.symbol,
        'price': cur.price,
        '1d_change': cur.daily_price_change_pct,
        '7d_change': cur.weekly_price_change_pct
    } for cur in currency.objects.order_by('-market_cap')[:count]], safe=False)

@csrf_exempt
def get_currencies_info(req, page):
    up_bound = first_currency_id + page_size * page
    currencies = currency.objects.filter(id__lt=up_bound).filter(id__gte=up_bound-page_size)
    return JsonResponse([{
        'symbol': cur.symbol,
        'price': cur.price,
        '1d_change': cur.daily_price_change_pct,
        '7d_change': cur.weekly_price_change_pct
    } for cur in currencies], safe=False)

@csrf_exempt
def get_currency_info(req, symbol):
    cur = currency.objects.get(symbol=symbol)
    return JsonResponse({
        'symbol': cur.symbol,
        'price': cur.price,
        '1d_change': cur.daily_price_change_pct,
        '7d_change': cur.weekly_price_change_pct,
        'turnover': cur.turnover,
        'market_cap': cur.market_cap,
    })