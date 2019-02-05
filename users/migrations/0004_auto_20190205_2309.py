# Generated by Django 2.1.5 on 2019-02-05 23:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190205_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='followed_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
