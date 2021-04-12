from django.contrib import admin
from .models import twit, report


@admin.register(twit)
class TwitAdmin(admin.ModelAdmin):
    verbose_name_plural = 'توییت ها'
    search_fields = ('id', )


@admin.register(report)
class ReportAdmin_(admin.ModelAdmin):
    verbose_name_plural = 'ریپورت ها'
    search_fields = ('Type', 'status')
    readonly_fields = ('twit_info', )