from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import pytz, mysql.connector, os
from datetime import datetime
from mimetypes import guess_type
from .models import twit
from home.models import currency
from utils.date_convertor import gregorian_to_shamsi
from home.views import which_currency

#connect to database (because mysql.connector.django can not save emojis)
mydb = mysql.connector.connect(
  host=os.getenv('DATABASE_HOST'),
  port=os.getenv('DATABASE_PORT'),
  user=os.getenv('DATABASE_USER_NAME'),
  password=os.getenv('DATABASE_USER_PASSWORD'),
  database=os.getenv('DATABASE_NAME'),
)


def tweets(req):
    if twit.objects.count() == 0 :
        last_tweets = []
    else:
        last_tweets = twit.objects.filter(id__gte=twit.objects.last().id-15).order_by('-id')
        # get text of tweets
        mycursor = mydb.cursor()
        mycursor.execute(f"select text from twits_twit where id>={last_tweets.last().id} order by -id")
        texts = mycursor.fetchall()
        print(mycursor)
        i=0
        for t in last_tweets:
            t.text =  texts[i][0]
            i+=1
    return render(req, 'tweet.html', {
        'tweets':last_tweets,
        'top_curs':currency.objects.all()[:10],
        'newyork_time':f"{datetime.now(pytz.timezone('America/New_York')).hour:02}:{datetime.now(pytz.timezone('America/New_York')).minute:02}",
        'tokyo_time':f"{datetime.now(pytz.timezone('Asia/Tokyo')).hour:02}:{datetime.now(pytz.timezone('Asia/Tokyo')).minute:02}",
        'hongkong_time':f"{datetime.now(pytz.timezone('Hongkong')).hour:02}:{datetime.now(pytz.timezone('Hongkong')).minute:02}",
        'london_time':f"{datetime.now(pytz.timezone('Europe/London')).hour:02}:{datetime.now(pytz.timezone('Europe/London')).minute:02}",
        })


def curr_tweets(req, curr_name):
    curr = currency.objects.get(name=curr_name)
    #check if there is any tweets
    if curr.twit_set.count() == 0:
        last_tweets = []
    else:
        last_tweets = curr.twit_set.all().filter(id__gte=curr.twit_set.last().id-15).order_by('-id')
        # get text of tweets
        mycursor = mydb.cursor()
        mycursor.execute(f"select text from twits_twit where id>={last_tweets.last().id} order by -id")
        texts = mycursor.fetchall()
        i=0
        for t in last_tweets:
            t.text =  texts[i][0]
            i+=1
    return render(req, 'curr_tweet.html', {
        'tweets':last_tweets, 
        'currency':curr, 
        'top_curs':currency.objects.all()[:10],
        'newyork_time':f"{datetime.now(pytz.timezone('America/New_York')).hour:02}:{datetime.now(pytz.timezone('America/New_York')).minute:02}",
        'tokyo_time':f"{datetime.now(pytz.timezone('Asia/Tokyo')).hour:02}:{datetime.now(pytz.timezone('Asia/Tokyo')).minute:02}",
        'hongkong_time':f"{datetime.now(pytz.timezone('Hongkong')).hour:02}:{datetime.now(pytz.timezone('Hongkong')).minute:02}",
        'london_time':f"{datetime.now(pytz.timezone('Europe/London')).hour:02}:{datetime.now(pytz.timezone('Europe/London')).minute:02}",
        })


@login_required(login_url='login')
def tweet(req):
    File = req.FILES.get('file')
    if File and File.size > 1000000:
        return redirect('tweets')
    if not req.POST['text']:
        return redirect('tweets')
    cur = which_currency(req.POST.get('currency'))
    if not cur:
        cur = currency.objects.filter(persian_name=req.POST.get('currency'))
    t = twit(
        text = '',
        currency= cur,
        user = req.user,
        has_image = guess_type(File.name)[0].split('/')[0] == 'image' if File else False,
        File = File,
        date = timezone.now(),
        shamsi_date = gregorian_to_shamsi(timezone.now()),
    )
    t.save()
    #save twit text seprately
    mycursor = mydb.cursor()
    mycursor.execute(f"update twits_twit set text='{req.POST['text']}' where id={t.id}")
    mydb.commit()
    if req.POST.get('curr_tweet'):
        return redirect('curr_tweets', req.POST['currency'])
    return redirect('tweets')


@login_required(login_url='login')
@csrf_exempt
def retweet(req, ID):
    File = req.FILES.get('file')
    if File and File.size > 1000000:
        return redirect('tweets')
    if not req.POST['text']:
        return redirect('tweets')
    reply_to = twit.objects.get(id=ID)
    t = twit(
        text = '',
        user = req.user,
        currency= reply_to.currency,
        retwit=True,
        reply_to = reply_to,
        date = timezone.now(),
        shamsi_date = gregorian_to_shamsi(timezone.now()),
    )
    if File:
        if req.POSTget('image'):
            t.has_image = True
        t.File = File
    t.save()
    #save twit text seprately
    mycursor = mydb.cursor()
    mycursor.execute(f"update twits_twit set text='{req.POST['text']}' where id={t.id}")
    mydb.commit()
    if req.POST.get('curr_tweet'):
        return redirect('curr_tweets', req.POST['currency'])
    return redirect('tweets')


##############  APIs   ##########################

def last_twits(req):
    last_id = int(req.GET['last_id'])
    twits = twit.objects.filter(id__gt=last_id)
    #serialize twits
    datas = []
    for t in twits:
        data = {
           'id': t.id,
           'text': t.text,
           'currency': t.currency,
           'username': t.user.username,
           'fullname': t.user.name,
           'user_image': t.user.image.url,
           'time': t.time,
           'has_image': t.has_image,
           'likes': t.likes.count(),
           'is_retwit': t.retwit
       } 
        if t.File:
            data['file'] = t.File.url
        if t.retwit:
            data['retwit'] = {
               'id': t.reply_to.id,
               'text': t.reply_to.text,
               'username': t.reply_to.user.username,
               'fullname': t.reply_to.user.name,
               'currency': t.reply_to.currency
            }
        datas.append(data)
    print(datas[-1]['text'])
    return JsonResponse(datas, safe=False)


@login_required(login_url='login')
@csrf_exempt
def like_tweet(req, ID):
    Tweet = twit.objects.get(id=ID)
    #remove like
    if Tweet.likes.filter(username=req.user.username):
        Tweet.likes.remove(req.user)
        return JsonResponse({'status':'dislike'})
    #like
    Tweet.likes.add(req.user)
    return JsonResponse({'status':'like'})
