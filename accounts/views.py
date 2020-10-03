from django.shortcuts import render
from django.contrib import auth
from django.utils import timezone
from django.http import JsonResponse
import random
from smtplib import SMTP_SSL
from .models import user

#email info for verifaction code
o = SMTP_SSL('mail.applier.ir', 465)
def send_email(reciever, code, sender='info@applier.ir'):
    o.connect('mail.applier.ir', 465)
    message = f"""From: crypto <{sender}>
    To: To Person <{reciever}>
    Subject: SMTP e-mail test

    your code to sign up in crypto:
    {code}
    """
    o.login('info@applier.ir', '4420888024ZyDJnYe5')
    o.sendmail(sender, reciever, message)


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
        return 1
        data = {'tab':'register', 'username':req.POST.get('username'), 'phone':req.POST.get('phone'), 'email':req.POST.get('email'), 'password':req.POST.get('password'), 'cnf_password':req.POST.get('cnf_password'), 'name':req.POST.get('name'), 'invite_code':req.POST.get('invite_code')}
        #the first submit of user(info)
        if req.POST.get('submit') == 'info':
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
                    print(User)
                    User = User[0]
                    User.username = data.get('username')
                    User.email = data.get('email')
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
                send_email(User.email, User.verify_code)
                data.update({'submit':'verify'})
                return render(req, 'register.html', data)
            except Exception as e:
                print('!!!!!!!!!!!!!!!!', e)
                data.update({'submit':'info', 'error':'ایمیل نادرست است!'})
                return render(req, 'register.html', data)

        #verification submit
        elif req.POST.get('submit') == 'verify':
            User = user.objects.get(phone=data.get('phone'))
            #check verification code
            if req.POST.get('verification_code') != str(User.verify_code):
                data.update({'submit':'verify', 'error':'کد وارد شده صحیح نیست!'})
                return render(req, 'register.html', data)
            if (timezone.now()-User.verify_code_time).total_seconds()>120:
                data.update({'submit':'verify', 'error':'time is out'})
                return render(req, 'register.html', data)
            #check invite code
            if data.get('invite_code'):
                print('yes i am in!!!1')
                introducer = user.objects.filter(invite_code=data.get('invite_code'))
                if not introducer:
                    data.update({'submit':'verify', 'error':'کد معرف صحیح نمی باشد.'})
                    return render(req, 'register.html', data)
                User.introducer = introducer[0]
            User.verified_phone = True
            User.save()
            auth.login(req, User)
            return render(req, 'index.html')
            

def validate_username(req):
    print('!!!!!!!!!!!!!!', req.GET.get('username'))
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