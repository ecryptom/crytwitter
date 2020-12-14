from django.urls import path
from .views import last_twits, ajax

urlpatterns = [
    path('last_twits', last_twits, name='last_twits'),
    path('ajax', ajax)
]