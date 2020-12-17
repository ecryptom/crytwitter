# Generated by Django 2.0 on 2020-12-17 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20201217_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='shamsi_joined_date',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='profiles/default-user.jpg', upload_to='profiles'),
        ),
    ]
