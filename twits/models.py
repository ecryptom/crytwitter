from django.db import models

class twit(models.Model):
    text = models.TextField(default='')
    currency = models.CharField(max_length=15)
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE, related_name='twits')
    time = models.DateTimeField(auto_now=True)
    retwit = models.BooleanField(default=False)
    reply_to = models.ForeignKey('twit',null=True, blank=True, on_delete=models.SET_NULL)
    File = models.FileField(upload_to='files', null=True, blank=True)
    has_image = models.BooleanField(default=False)
    likes = models.ManyToManyField('accounts.user', related_name='twit_likes')

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



