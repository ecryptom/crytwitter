from django.contrib import admin
from .models import article, article_chunk, faq

#admin.site.register(article)
#admin.site.register(article_chunk)

@admin.register(article)
class ArticleAdmin_(admin.ModelAdmin):
    verbose_name_plural = 'مقالات'


@admin.register(article_chunk)
class ChunkArticleAdmin_(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'article']
    ordering = ['article', 'number']


@admin.register(faq)
class FaqAdmin(admin.ModelAdmin):
    verbose_name_plural = 'سوالات متداول'
