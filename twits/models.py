from django.db import models
from django.utils import timezone

class twit(models.Model):
    text = models.TextField(default='')
    currency = models.ForeignKey('home.currency', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE, related_name='twits')
    time = models.DateTimeField(auto_now=True)
    retwit = models.BooleanField(default=False)
    reply_to = models.ForeignKey('twit',null=True, blank=True, on_delete=models.SET_NULL)
    File = models.FileField(upload_to='files', null=True, blank=True)
    has_image = models.BooleanField(default=False)
    likes = models.ManyToManyField('accounts.user', related_name='twit_likes')
    date = models.DateTimeField()
    shamsi_date = models.CharField(max_length=11, default="1399/11/26")

    class Meta:
        verbose_name_plural = 'توییت‌ها'


class comment(models.Model):
    text = models.TextField(default='')
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE, related_name='comments')
    time = models.DateTimeField(auto_now=True)
    reply_to = models.ForeignKey('twit', on_delete=models.CASCADE, related_name='comments')
    File = models.FileField(upload_to='files', null=True, blank=True)
    likes = models.ManyToManyField('accounts.user', related_name='commect_likes')

    class Meta:
        verbose_name_plural = 'کامنت توییت‌ها'


class report(models.Model):
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE)
    twit = models.ForeignKey('twits.twit', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now())
    Type = models.CharField(choices=(('تبلیغ', 'تبلیغ'), ('تکرار', 'تکرار'), ('توهین', 'توهین')), max_length=5)
    status = models.CharField(choices=(('رد', 'رد'), ('پذیرفته', 'پذیرفته'), ('ندیده', 'ندیده')), default='ندیده', max_length=8)
    

    def twit_info(self):
        return f'''
        twit_id = {self.twit.id}
        username = {self.twit.user.username}
        twit_text = {self.twit.text}
        '''



