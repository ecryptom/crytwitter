from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import twit
from home.models import currency

def tweets(req):
    last_tweets = twit.objects.filter(id__gte=twit.objects.last().id-15).order_by('-id')
    return render(req, 'tweet.html', {'tweets':last_tweets})

@login_required(login_url='login')
def tweet(req):
    File = req.FILES.get('file')
    if File and File.size > 1000000:
        return redirect('tweets')
    if not req.POST['text']:
        return redirect('tweets')
    cur = currency.objects.filter(name=req.POST.get('currency'))
    if not cur:
        cur = currency.objects.filter(persian_name=req.POST.get('currency'))
    t = twit(
        text = req.POST['text'],
        currency= cur[0] if cur else None,
        user = req.user
    )
    if File:
        if req.POSTget('image'):
            t.has_image = True
        t.File = File
    t.save()
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
