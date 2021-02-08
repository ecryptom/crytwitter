from django.contrib import admin
from .models import article, article_chunk

#admin.site.register(article)
#admin.site.register(article_chunk)

@admin.register(article)
class ArticleAdmin_(admin.ModelAdmin):
    verbose_name_plural = 'مقالات'


@admin.register(article_chunk)
class ArticleAdmin_(admin.ModelAdmin):
    ordering = ['article', 'number']
