from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from crypto import settings
from django.template.loader import render_to_string
import random, requests, os, json
from .models import user
from home.models import currency, dollor
from home.views import which_currency

forgot_password_text = lambda code : f'کد بازیابی رمز عبور شما در سایت ارزتوییتر : \n {code}'
sms_text = lambda code : f'کد تایید ورود شما به سایت ارز توییتر:\n {code}'
sms_signature = os.getenv('sms_signature')

#verify recactcha response
def verify_recaptcha(token):
    result = requests.get('https://www.google.com/recaptcha/api/siteverify',{
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': token,
    })
    return json.loads(result.content.decode())['success']



def login(req):
    if req.method == 'GET':
        return render(req, 'login.html', {
            'next': req.GET.get('next') if req.GET.get('next') else '',
            'recaptcha': settings.GOOGLE_RECAPTCHA_SITE_KEY,
        })
    #check recaptcha 
    if not verify_recaptcha(req.POST['g-recaptcha-response']):
        return render(req, 'login.html', {
            'error':'لطفا کد امنیتی را تکمیل و مجدد اقدام کنید',
            'next': req.POST.get('next'),
            'recaptcha': settings.GOOGLE_RECAPTCHA_SITE_KEY,
        })
    username = req.POST.get('username')
    password = req.POST.get('password')
    next_page = req.POST.get('next') if req.POST.get('next') else 'home'
    #check username
    User = auth.authenticate(username=username, password=password)
    if User and User.verified_phone:
        auth.login(req, User)
        return redirect(next_page)
    #check phone
    User = user.objects.filter(phone=username)
    if User and User[0].verified_phone:
        #check password
        if User[0].check_password(password):
            auth.login(req, User[0])
            return redirect(next_page)
        else:
            return render(req, 'login.html', {
                'error':'رمز عبور اشتباه است',
                'next': req.POST.get('next'),
                'recaptcha': settings.GOOGLE_RECAPTCHA_SITE_KEY,
                })
    #else return error
    return render(req, 'login.html', {
        'error':'کاربری با این اطلاعات وجود ندارد',
        'next': req.POST.get('next'),
        'recaptcha': settings.GOOGLE_RECAPTCHA_SITE_KEY,
        })
    
def logout(req):
    auth.logout(req)
    return redirect('home')

def register(req, invite_code=''):
    if req.method == 'GET':
        return render(req, 'register.html', {
            'submit':'info', 
            'invite_code':invite_code, 
            'tab':'register',
            'recaptcha':settings.GOOGLE_RECAPTCHA_SITE_KEY,
            })
    else:
        data = {'username':req.POST.get('username'), 
        'phone':req.POST.get('phone'), 
        'password':req.POST.get('password'), 
        'cnf_password':req.POST.get('cnf_password'), 
        'name':req.POST.get('name'), 
        'invite_code':req.POST.get('invite_code'),
        'recaptcha':settings.GOOGLE_RECAPTCHA_SITE_KEY,
        }
        #check recaptcha 
        if not verify_recaptcha(req.POST['g-recaptcha-response']):
            data.update({'submit':'info', 'error':'لطفا کد امنیتی را تکمیل و مجدد اقدام کنید'})
            return render(req, 'register.html', data)
        #check username
        User = user.objects.filter(username=data.get('username'))
        if User:
            if User[0].verified_phone:
                data.update({'submit':'info', 'error':'این نام کاربری قبلا ثبت شده است'})
                return render(req, 'register.html', data)
            else:
                User[0].delete()
        #check password confirm
        if data.get('password') != data.get('cnf_password'):
            data.update({'submit':'info', 'error':'رمز عبور با تکرار آن همخوانی ندارد!'})
            return render(req, 'register.html', data)
        #check invite code
        if data.get('invite_code'):
            introducer = user.objects.filter(invite_code=data.get('invite_code'))
            if not introducer:
                introducer = None
                data.update({'submit':'info', 'error':'کد معرف صحیح نمی باشد!'})
                return render(req, 'register.html', data)
            introducer = introducer[0]
        else:
            introducer = None
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
                User.name = data.get('name')
                User.introducer = introducer
                User.save()
        #create new user
        if not User:
            User = user.objects.create_user(data.get('username'), data.get('phone'), data.get('password'), data.get('name'), introducer)
        #create and send verification code
        User.verify_code = random.randint(10000, 99999)
        User.verify_code_time = timezone.now()
        User.save()
        try:
            requests.get(f'http://sms.parsgreen.ir/UrlService/sendSMS.ashx?from=10001398&to={User.phone}&&text={sms_text(User.verify_code)}&signature={sms_signature}')
            return render(req, 'verify.html', {'phone':User.phone, 'seconds':119})
        except:
            data.update({'error':'شماره تلفن نادرست است!'})
            return render(req, 'register.html', data)


def verify_code(req):
    User = user.objects.get(phone=req.POST.get('phone'))
    #check verification code
    if (timezone.now()-User.verify_code_time).total_seconds()>120:
        return render(req, 'verify.html', {'phone': User.phone, 'error': 'زمان وارد کردن کد تایید بیش از حد مجاز', 'seconds':0})
    if req.POST.get('verification_code') != str(User.verify_code):
        return render(req, 'verify.html', {'phone': User.phone, 'error': 'کد تایید اشتباه است', 'seconds':int(119-(timezone.now()-User.verify_code_time).total_seconds())})
    User.verified_phone = True
    User.save()
    auth.login(req, User) 
    return redirect('home')
    


def resend_phone_code(req):
    User = user.objects.get(phone=req.GET.get('phone'))
    User.verify_code = random.randint(10000, 99999)
    User.verify_code_time = timezone.now()
    User.save()
    try:
        requests.get(f'http://sms.parsgreen.ir/UrlService/sendSMS.ashx?from=10001398&to={User.phone}&&text={sms_text(User.verify_code)}&signature={sms_signature}')
        return render(req, 'verify.html', {'phone': User.phone, 'seconds':119})
    except:
        return JsonResponse({'status':'failed'})



def forgot_password(req):
    if req.method == 'GET':
        return render(req, 'forgot_password.html', {
            'step':'get_phone', 
            'recaptcha':settings.GOOGLE_RECAPTCHA_SITE_KEY,
            'phone': req.GET.get('phone'),
        })

    # step: get_phone
    if req.POST['step'] == 'get_phone':
        #check recaptcha 
        if not verify_recaptcha(req.POST['g-recaptcha-response']):
            return render(req, 'forgot_password.html', {
                    'step':'get_phone', 
                    'error':'لطفا کد امنیتی را تکمیل و مجدد اقدام کنید',
                    'recaptcha':settings.GOOGLE_RECAPTCHA_SITE_KEY,
                })
        User = user.objects.filter(phone=req.POST['phone'])
        if not User:
            return render(req, 'forgot_password.html', {
                'step':'get_phone', 
                'error':'کاربری با این شماره وجود ندارد',
                'recaptcha':settings.GOOGLE_RECAPTCHA_SITE_KEY,
                })
        #set and send verification code
        try:
            User[0].verify_code = random.randint(10000, 99999)
            User[0].verify_code_time = timezone.now()
            User[0].save()
            requests.get(f'http://sms.parsgreen.ir/UrlService/sendSMS.ashx?from=10001398&to={User[0].phone}&&text={forgot_password_text(User[0].verify_code)}&signature={sms_signature}')
            return render(req, 'forgot_password.html', {'step':'get_verification_code', 'phone':User[0].phone, 'message':'کد ارسال شده را وارد کنید'})
        except:
            return render(req, 'forgot_password.html', {
                'step':'get_phone', 
                'error':'شماره تلفن وارد شده صحیح نمی باشد',
                'recaptcha':settings.GOOGLE_RECAPTCHA_SITE_KEY,
                })
    
    # step: get_verification_code
    if req.POST['step'] == 'get_verification_code':
        code = req.POST['verification_code']
        User = user.objects.get(phone=req.POST['phone'])
        if str(User.verify_code) == code:
            return render(req, 'forgot_password.html', {'step':'change_password', 'phone':User.phone, 'verification_code':code})
        else:
            return render(req, 'forgot_password.html', {'step':'get_verification_code', 'phone':User.phone, 'error':'کد وارد شده صحیح نمی باشد'})

    # step: change password
    if req.POST['step'] == 'change_password':
        code = req.POST['verification_code']
        User = user.objects.get(phone=req.POST['phone'])
        if str(User.verify_code) == code:
            User.set_password(req.POST['new_password'])
            User.save()
            return render(req, 'login.html', {
                'message':'رمز عبور با موفقیت تغییر کرد',
                'recaptcha': settings.GOOGLE_RECAPTCHA_SITE_KEY,
                })




@login_required(login_url='login')
def dashboard(req):
    return render(req, 'panel-dashboard.html')

@login_required(login_url='login')
def change_pass(req):
    if req.method == 'GET':
        return render(req, 'panel-change-password.html')
    if not req.user.check_password(req.POST.get('old_pass')):
        return render(req, 'panel-change-password.html', {'error':'رمز عبور فعلی اشتباه است'})
    if req.POST['new_pass'] != req.POST['cnf_new_pass']:
        return render(req, 'panel-change-password.html', {'error':'رمز عبور جدید با تکرار آن مطابق نیست'})
    req.user.set_password(req.POST['new_pass'])
    req.user.save()
    auth.login(req, req.user)
    return render(req, 'panel-change-password.html', {'message': 'رمز عبور با موفقیت تغییر کرد'})

@login_required(login_url='login')
def edit_profile(req):
    User = req.user
    if req.method == 'GET':
        if User.email and not User.verified_email:
            return render(req, 'panel-edit-profile.html', {'message': 'شما هنوز ایمیل خود را تایید نکرده اید', 'mode':'warning'})
        if not User.email:
            return render(req, 'panel-edit-profile.html', {'message': 'لطفا ایمیل خود را وارد کرده و آن را تایید نمایید', 'mode':'warning'})
        return render(req, 'panel-edit-profile.html')

    #redirect to verification page
    if req.POST['submit'] == 'verify_email':
        User.verify_code = random.randint(10000, 99999)
        User.verify_code_time = timezone.now()
        User.save()
        message = render_to_string('emails/email_verification.html', {'code':User.verify_code})
        send_mail(
            subject='verify',
            message='',
            html_message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[User.email]
        )
        return render(req, 'verify_email.html', {'email': User.email, 'seconds':119})

    #save post data
    else:
        #change name
        User.name = req.POST['name']
        #change image
        if req.FILES.get('image'):
            User.image = req.FILES.get('image')
        User.save()
        #change email
        email = req.POST['email']
        if email != req.user.email:
            if '@' not in email or '.' not in email:
                return render(req, 'panel-edit-profile.html', {'message': 'ایمیل نامعتبر است', 'mode':'danger'})
            User.email = email
            User.verified_email = False
            User.save()
            return render(req, 'panel-edit-profile.html', {'message': 'لطفا ایمیل خود را تایید کنید', 'mode':'info'})
        return render(req, 'panel-edit-profile.html')


def verify_email_code(req):
    User = user.objects.get(email=req.POST.get('email'))
    #check verification code
    if (timezone.now()-User.verify_code_time).total_seconds()>120:
        return render(req, 'verify_email.html', {'email': User.email, 'error': 'زمان وارد کردن کد تایید بیش از حد مجاز', 'seconds':0})
    if req.POST.get('verification_code') != str(User.verify_code):
        return render(req, 'verify_email.html', {'email': User.email, 'error': 'کد تایید اشتباه است', 'seconds':int(119-(timezone.now()-User.verify_code_time).total_seconds())})
    User.verified_email = True
    User.save()
    auth.login(req, User) 
    return render(req, 'panel-edit-profile.html', {'message': 'ایمیل با موفقیت تایید شد', 'mode':'info'})


def resend_email_code(req):
    User = user.objects.get(email=req.GET.get('email'))
    User.verify_code = random.randint(10000, 99999)
    User.verify_code_time = timezone.now()
    User.save()
    try:
        message = render_to_string('emails/email_verification.html', {'code':User.verify_code})
        send_mail(
            subject='verify',
            message='',
            html_message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[User.email]
        )
        return render(req, 'verify_email.html', {'email': User.email, 'seconds':119})
    except:
        return JsonResponse({'status':'failed'})



@login_required(login_url='login')
def invite_friends(req):
    return render(req, 'panel-invite-friends.html', {'users':req.user.invited_set.filter(verified_phone=True)})


@login_required(login_url='login')
def watch_list_page(req):
    Watch_list = req.user.watch_list.all()
    symbols = ','.join([cur.symbol for cur in Watch_list])
    return render(req, 'watch-list.html', {'watch_list': Watch_list, 'symbols':symbols, 'dollor_rate':dollor.objects.get().rate})

@login_required(login_url='login')
def add_watch_list(req):
    cur = which_currency(req.POST['currency'])
    if cur and not req.user.watch_list.filter(id=cur.id):
        req.user.watch_list.add(cur) 
    return redirect('watch_list_page')

@login_required(login_url='login')
def remove_watch_list(req, ID):
    cur = currency.objects.get(id=ID)
    req.user.watch_list.remove(cur)
    return redirect('watch_list_page')



##########  APIs   ############

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



@csrf_exempt
@login_required(login_url='login')
def get_watch_list_market_info(req):
    return JsonResponse([{
        'symbol': cur.symbol,
        'price': cur.price,
        '1d_change': cur.daily_price_change_pct,
        '7d_change': cur.weekly_price_change_pct
    } for cur in req.user.watch_list.all()], safe=False)
    
