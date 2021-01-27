from django.db import models

class currency(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=15)
    persian_name = models.BinaryField()
    image_url = models.URLField()
    price = models.IntegerField(default=56)
    daily_price_change_pct = models.FloatField(default=-0.01)
    weekly_price_change_pct = models.FloatField(default=1.5)
    

class dollor(models.Model):
    rate = models.IntegerField()