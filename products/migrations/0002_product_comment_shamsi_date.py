# Generated by Django 2.0 on 2020-12-18 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_comment',
            name='shamsi_date',
            field=models.CharField(default='1399/9/28', max_length=11),
        ),
    ]
