# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-10-15 04:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAuth', '0002_customuser_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='pic',
            field=models.ImageField(default='media/index.png', upload_to='media/'),
        ),
    ]
