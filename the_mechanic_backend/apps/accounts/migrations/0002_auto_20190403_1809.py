# Generated by Django 2.1.5 on 2019-04-03 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='email',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='store',
            name='phone',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='store',
            name='website',
            field=models.CharField(default='', max_length=200),
        ),
    ]
