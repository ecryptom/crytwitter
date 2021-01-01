from django.db import models

class currency(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=15)
    persian_name = models.BinaryField()
    image_url = models.URLField()
