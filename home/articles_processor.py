from .models import article

def get_articles(request):
    articles = article.objects.all()
    return {'articles': articles}
