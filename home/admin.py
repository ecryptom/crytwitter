from django.contrib import admin
from .models import article, article_chunk, faq, index_comments

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
    pass

@admin.register(index_comments)
class FaqAdmin(admin.ModelAdmin):
    pass