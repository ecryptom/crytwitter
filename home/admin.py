from django.contrib import admin
from .models import article, faq, index_comments

#admin.site.register(article)
#admin.site.register(article_chunk)

@admin.register(article)
class ArticleAdmin_(admin.ModelAdmin):
    verbose_name_plural = 'مقالات'
    search_fields = ('has_menu',)
    readonly_fields = ('split_tags', )


@admin.register(faq)
class FaqAdmin(admin.ModelAdmin):
    pass

@admin.register(index_comments)
class FaqAdmin(admin.ModelAdmin):
    pass
