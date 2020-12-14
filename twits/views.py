from django.shortcuts import render
from django.http import JsonResponse
from .models import twit

def twits(req):
    twits = twit.objects.filter(id__gte=twit.objects.last().id-15)
    return render(req, 'twits.html',{'twits':twits})

def tweet(req):
    File = req.FILES.get['file']
    if File and File.size > 1000000:
        return False                             #...
    t = twit(
        text = req.POST['text'].encode(),
        currency= req.POST['currency'],
        user = req.user,
        retwit = req.POST['is_retwit'],
        reply_to = twit.objects.get(id=req.POST['retwit_id'])
    )
    if File:
        if req.POST['image']:
            t.has_image = True
        t.File = File
    t.save()


def last_twits(req):
    last_id = int(req.GET['last_id'])
    twits = twit.objects.filter(id__gt=last_id)
    #serialize twits
    datas = []
    for t in twits:
        data = {
           'id': t.id,
           'text': t.text.decode(),
           'currency': t.currency,
           'username': t.user.username,
           'fullname': t.user.name.decode(),
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
               'text': t.reply_to.text.decode(),
               'username': t.reply_to.user.username,
               'fullname': t.reply_to.user.name.decode(),
               'currency': t.reply_to.currency
            }
        datas.append(data)
    print(datas[-1]['text'])
    return JsonResponse(datas, safe=False)

def ajax(req):
    return render(req, 'ajax.html')