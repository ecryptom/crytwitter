from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class alaki(models.Model):
    text = RichTextUploadingField()

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
    image = models.ImageField(upload_to='articles', verbose_name='تصویر اصلی', default='ali')
    content = RichTextUploadingField(default='')
    has_menu = models.BooleanField(default=False, verbose_name='آنچه در این مقاله می خوانید')
    tags = models.CharField(max_length=100, default='مقاله;بیت کوین;ارزتوییتر;crypto', null=True, verbose_name='تگ ها(با علامت ; جدا شوند)')
    date = models.DateField(auto_now=True, verbose_name="تاریخ")
    views = models.ManyToManyField('accounts.user', null=True, blank=True, verbose_name='بازدیدها')

    def split_tags(self):
        return self.tags.split(';')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'مقالات'





    


class article_comment(models.Model):
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE)
    article = models.ForeignKey(article, on_delete=models.CASCADE)
    shamsi_date = models.CharField(max_length=11)
    text = models.TextField()
    reply_to = models.ForeignKey('home.article_comment', related_name='replies_in', on_delete=models.CASCADE, null=True)



class faq(models.Model):
    question = models.TextField(verbose_name='سوال')
    answer = models.TextField(verbose_name='جواب')
    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name_plural = '<سوالات متداول>'


class index_comments(models.Model):
    name = models.CharField(max_length=25 ,verbose_name='نام کاربر')
    position = models.CharField(max_length=25 ,verbose_name='عنوان')
    text = models.TextField(verbose_name='متن نظر')
    image = models.ImageField(upload_to='profiles', null=True, blank=True, verbose_name='تصویر(اختیاری)')
    def __str__(self):
        return self.name + '_' + self.position
    
    class Meta:
        verbose_name_plural = 'نظرات کاربران'