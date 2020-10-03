from django.urls import path, include
from .views import register, login, validate_email, validate_invite_code, validate_phone, validate_username

urlpatterns = [
    path('login', login, name='login'),
    path('register/<str:invite_code>', register, name='register_code'),
    path('register', register, name='register'),
    path('validate_email', validate_email),
    path('validate_invite_code', validate_invite_code),
    path('validate_phone', validate_phone),
    path('validate_username', validate_username),
]