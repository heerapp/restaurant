# Generated by Django 3.1.4 on 2021-02-26 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210225_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='onorder',
            name='address',
            field=models.CharField(default='address', max_length=100),
        ),
        migrations.AddField(
            model_name='onorder',
            name='contact',
            field=models.CharField(default='123456789', max_length=50),
        ),
    ]
