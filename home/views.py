from django.shortcuts import render


def home(req):
    return render(req, 'index.html')

def page_resp(req, page):
    return render(req, page)