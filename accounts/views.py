from django.shortcuts import render
from django.contrib import auth
from django.utils import timezone
from django.http import JsonResponse
import random, requests
from .models import user




def login(req):
    if req.method == 'GET':
        return render(req, 'register.html', {'tab':'login'})
    username = req.POST.get('username')
    password = req.POST.get('password')
    #check username
    User = auth.authenticate(username=username, password=password)
    if User:
        auth.login(req, User)
        return render(req, 'index.html')
    #check phone
    User = user.objects.filter(phone=username)
    if User and User[0].check_password(password) and User[0].verified_phone:
        auth.login(req, User[0])
        return render(req, 'index.html')
    #check email
    User = user.objects.filter(email=username)
    if User and User[0].check_password(password) and  User.verified_email:
        auth.login(req, User[0])
        return render(req, 'index.html')
    #else return error
    return render(req, 'register.html', {'tab':'login', 'error':'کاربری با این اطلاعات وجود ندارد'})
    


def register(req, invite_code=''):
    if req.method == 'GET':
        return render(req, 'register.html', {'submit':'info', 'invite_code':invite_code, 'tab':'register'})
    else:
        data = {'tab':'register', 'username':req.POST.get('username'), 'phone':req.POST.get('phone'), 'email':req.POST.get('email'), 'password':req.POST.get('password'), 'cnf_password':req.POST.get('cnf_password'), 'name':req.POST.get('name'), 'invite_code':req.POST.get('invite_code')}
        #check username
        User = user.objects.filter(username=data.get('username'))
        if User:
            if User[0].verified_phone:
                data.update({'submit':'info', 'error':'این نام کاربری قبلا ثبت'})
                return render(req, 'register.html', data)
            else:
                User[0].delete()
        #check password confirm
        if data.get('password') != data.get('cnf_password'):
            data.update({'submit':'info', 'error':'رمز عبور با تکرار آن همخوانی ندارد!'})
            return render(req, 'register.html', data)
        #check invite code
        if data.get('invite_code') and not user.objects.filter(invite_code=data.get('invite_code')):
            data.update({'submit':'info', 'error':'کد معرف صحیح نمی باشد!'})
            return render(req, 'register.html', data)
        #check phone number
        User = user.objects.filter(phone=data.get('phone'))
        if User:
            if User[0].verified_phone:
                data.update({'submit':'info', 'error':'این شماره تلفن قبلا ثبت شده است!'})
                return render(req, 'register.html', data)
            else:
                User = User[0]
                User.username = data.get('username')
                User.set_password(data.get('password'))
                User.name = data.get('name').encode()
                User.save()
        if not User:
            User = user.objects.create_user(data.get('username'), data.get('phone'), data.get('email'), data.get('password'), name=data.get('name').encode())
        #create and send verification code
        User.verify_code = random.randint(10000, 99999)
        User.verify_code_time = timezone.now()
        User.save()
        try:
            text = f'arztwitter verification code: {User.verify_code}'
            requests.get(f'http://sms.parsgreen.ir/UrlService/sendSMS.ashx?from=10001398&to={User.phone}&&text={text}&signature=0DBAC16D-54EA-4A7F-B200-4D5246409AAB')
            return render(req, 'verify.html', {'type':'phone', 'phone':User.phone})
        except Exception as e:
            data.update({'submit':'info', 'error':'شماره تلفن نادرست است!'})
            return render(req, 'register.html', data)


def verify_code(req):
    #verify phone
    if req.POST['type'] == 'phone':
        User = user.objects.get(phone=req.POST.get('phone'))
        #check verification code
        if req.POST.get('verification_code') != str(User.verify_code):
            return render(req, 'verify.html', {'type':'phone', 'phone': User.phone, 'error': 'کد تایید اشتباه است'})
        if (timezone.now()-User.verify_code_time).total_seconds()>120:
            return render(req, 'verify.html', {'type':'resend_phone', 'phone': User.phone, 'error': 'زمان وارد کردن کد تایید بیش از حد مجاز'})
        User.verified_phone = True
        User.save()
        auth.login(req, User) 
        return render('home.html')
    #verify email
    if req.POST['type'] == 'email':
        User = req.user
        #check verification code
        if req.POST.get('verification_code') != str(User.verify_code):
            return render(req, 'verify.html', {'type':'email', 'email': User.email, 'error': 'کد تایید اشتباه است'})
        if (timezone.now()-User.verify_code_time).total_seconds()>120:
            return render(req, 'verify.html', {'type':'resend_email', 'email': User.phone, 'error': 'زمان وارد کردن کد تایید بیش از حد مجاز'})
        User.verified_email = True
        User.save()
        return render('home.html')


def resend_phone_code(req):
    User = user.objects.get(phone=req.POST.get('phone'))
    User.verify_code = random.randint(10000, 99999)
    User.verify_code_time = timezone.now()
    User.save()
    try:
        text = f'arztwitter verification code: {User.verify_code}'
        requests.get(f'http://sms.parsgreen.ir/UrlService/sendSMS.ashx?from=10001398&to={User.phone}&&text={text}&signature=0DBAC16D-54EA-4A7F-B200-4D5246409AAB')
        return render(req, 'verify.html', {'type':'phone', 'phone': User.phone})
    except:
        return render(req, 'register.html')



            

def validate_username(req):
    User = user.objects.filter(username=req.GET.get('username'))
    status = 'available'
    if User and User[0].verified_phone:
        status = 'not-available'
    return JsonResponse({'status':status})

def validate_phone(req):
    User = user.objects.filter(phone=req.GET.get('phone'))
    status = 'available'
    if User and User[0].verified_phone:
        status = 'not-available'
    return JsonResponse({'status':status})

def validate_email(req):
    User = user.objects.filter(email=req.GET.get('email'))
    status = 'available'
    if User and User[0].verified_email:
        status = 'not-available'
    return JsonResponse({'status':status})

def validate_invite_code(req):
    User = user.objects.filter(invite_code=req.GET.get('invite_code'))
    status = 'not-available'
    if User and User[0].verified_phone:
        status = 'available'
    return JsonResponse({'status':status})