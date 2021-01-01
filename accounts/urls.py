from django.urls import path, include
from .views import *

urlpatterns = [
    path('login', login, name='login'),
    path('register/<str:invite_code>', register, name='register_code'),
    path('register', register, name='register'),
    path('logout', logout, name='logout'),
    path('verify_code', verify_code, name='verify_code'),
    path('resend_phone_code', resend_phone_code, name='resend_phone_code'),
    path('edit_profile', edit_profile, name='edit_profile'),
    path('dashboard', dashboard, name='dashboard'),
    path('change_pass', change_pass, name='change_pass'),
    path('edit_profile', edit_profile, name='edit_profile'),
    path('invite_friends', invite_friends, name='invite_friends'),
    path('verify_email', verify_email, name='verify_email'),
    path('watch_list_page', watch_list_page, name='watch_list_page'),
    path('add_watch_list', add_watch_list, name='add_watch_list'),

    ### APIs ###
    path('validate_email', validate_email),
    path('validate_invite_code', validate_invite_code),
    path('validate_phone', validate_phone),
    path('validate_username', validate_username),
    path('get_watch_list', get_watch_list, name='get_watch_list')
]