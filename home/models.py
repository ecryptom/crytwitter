from django.db import models

class currency(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=15)
    persian_name = models.CharField(max_length=50)
    image_url = models.URLField()
    price = models.FloatField(default=56.0)
    daily_price_change_pct = models.FloatField(default=-0.01)
    weekly_price_change_pct = models.FloatField(default=1.5)
    

class dollor(models.Model):
    rate = models.IntegerField()


class article(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    image = models.ImageField(upload_to='articles', verbose_name='تصویر اصلی', null=True, blank=True)
    introduction = models.TextField(null=True, blank=True, verbose_name='مقدمه')
    main_text = models.TextField(null=True, blank=True, verbose_name='متن اصلی')
    tags = models.CharField(max_length=100, default='مقاله;بیت کوین;ارزتوییتر;crypto', null=True, verbose_name='تگ ها(با علامت ; جدا شوند)')

    def split_tags(self):
        return self.tags.split(';')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'مقالات'




class article_chunk(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    text1 = models.TextField(verbose_name='متن قبل از تصویر', null=True, blank=True)
    image = models.ImageField(upload_to='articles', verbose_name='تصویر', null=True, blank=True)
    text2 = models.TextField(verbose_name='متن بعد از تصویر', null=True, blank=True)
    number = models.PositiveSmallIntegerField(verbose_name='شماره')
    article = models.ForeignKey('home.article', verbose_name='مقاله', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.article.title}_قسمت_{self.number}'

    class Meta:
        verbose_name_plural = 'بخش‌های مقالات'

    


class article_comment(models.Model):
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE)
    article = models.ForeignKey(article, on_delete=models.CASCADE)
    shamsi_date = models.CharField(max_length=11)
    text = models.TextField()
    reply_to = models.ForeignKey('home.article_comment', related_name='replies_in', on_delete=models.CASCADE, null=True)



