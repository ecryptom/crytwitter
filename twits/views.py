from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import pytz, mysql.connector, os
from datetime import datetime
from mimetypes import guess_type
from .models import twit, report
from home.models import dollor
from home.models import currency
from utils.date_convertor import gregorian_to_shamsi
from home.views import which_currency
from products.models import product_group
from accounts.models import user

try:
    #connect to database (because mysql.connector.django can not save emojis)
    mydb = mysql.connector.connect(
      host=os.getenv('DATABASE_HOST'),
      port=os.getenv('DATABASE_PORT'),
      user=os.getenv('DATABASE_USER_NAME'),
      password=os.getenv('DATABASE_USER_PASSWORD'),
      database=os.getenv('DATABASE_NAME'),
    )
    #global user
    arztwitter = user.objects.get(username='arztwitter')
except:
    pass

def tweets(req):
    #check if there is any tweets
    if twit.objects.count() == 0 :
        last_tweets = []
    else:
        last_tweets = twit.objects.filter(id__gte=twit.objects.last().id-15).order_by('-id')
        # get text of tweets
        mycursor = mydb.cursor()
        mycursor.execute(f"select text from twits_twit where id>={last_tweets.last().id} order by -id")
        texts = mycursor.fetchall()
        try:
            i=0
            for t in last_tweets:
                t.text =  texts[i][0]
                i+=1
        except:
            pass
    return render(req, 'tweet.html', {
        'tweets':last_tweets,
        'top_curs':currency.objects.order_by('-market_cap')[:10],
        'dollor_rate':dollor.objects.get().rate,
        'product_groups':product_group.objects.all(),
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
        mycursor.execute(f"select text from twits_twit where (id>={last_tweets.last().id}) and (currency_id={curr.id}) order by -id")
        texts = mycursor.fetchall()
        try:
            i=0
            for t in last_tweets:
                t.text =  texts[i][0]
                i+=1
        except:
            pass
    return render(req, 'tweet.html', {
        'tweets':last_tweets, 
        'currency':curr, 
        'dollor_rate':dollor.objects.get().rate,
        'product_groups':product_group.objects.all(),
        })



def tweet(req):
    #check user authentication
    if not req.user.is_authenticated:
        req.user = arztwitter
    #check file size
    File = req.FILES.get('file')
    if File and File.size > 3000000:
        return redirect('tweets')
    #check twit len
    if len(req.POST['text']) > 2000:
        return redirect('tweets')
    #check if twit is empty
    if not (req.POST['text'] or File):
        return redirect('tweets')
    #extract currency from user input
    cur = which_currency(req.POST.get('currency'))
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
    if req.user == arztwitter:
        return redirect('login')
    if req.POST.get('curr_tweet'):
        return redirect('curr_tweets', req.POST['currency'])
    return redirect('tweets')


@csrf_exempt
def retweet(req, ID):
    #check user authentication
    if not req.user.is_authenticated:
        req.user = arztwitter
    #check file size
    File = req.FILES.get('file')
    if File and File.size > 3000000:
        return redirect('tweets')
    #check twit len
    if len(req.POST['text']) > 2000:
        return redirect('tweets')
    #check if twit is empty
    if not (req.POST['text'] or File):
        return redirect('tweets')
    reply_to = twit.objects.get(id=ID)
    t = twit(
        text = '',
        user = req.user,
        has_image = guess_type(File.name)[0].split('/')[0] == 'image' if File else False,
        File = File,
        currency= reply_to.currency,
        retwit=True,
        reply_to = reply_to,
        date = timezone.now(),
        shamsi_date = gregorian_to_shamsi(timezone.now()),
    )
    t.save()
    #save twit text seprately
    mycursor = mydb.cursor()
    mycursor.execute(f"update twits_twit set text='{req.POST['text']}' where id={t.id}")
    mydb.commit()
    if req.user == arztwitter:
        return redirect('login')
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



@csrf_exempt
def report_req(req):
    #check authentication
    if not req.user.is_authenticated:
        return JsonResponse({'status':'error', 'message':'لطفا ابتدا وارد حساب کاربری خود شوید'})
    #check if report has been saved before
    Twit = twit.objects.get(id=req.GET['tweet_id'])
    if report.objects.filter(user=req.user).filter(twit=Twit).filter(Type=req.GET['type']):
        return JsonResponse({'status':'error', 'message':'گزارش تکراری'})
    #save report
    Report = report(
        twit = twit.objects.get(id=req.GET['tweet_id']),
        user = req.user,
        Type = req.GET['type'],
    )
    Report.save()
    return JsonResponse({'status':'success', 'message':'کاربر گرامی گزارش شما با موفقیت ثبت شد از کمک شما در راستای بهبود فضای ارز توییتر سپاسگذاریم.'})