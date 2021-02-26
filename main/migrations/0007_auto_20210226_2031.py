# Generated by Django 3.1.4 on 2021-02-26 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210226_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='onorder',
            name='address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='onorder',
            name='contact',
            field=models.CharField(max_length=50),
        ),
    ]
