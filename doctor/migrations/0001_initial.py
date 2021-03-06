# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-10-17 10:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorSlots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_date', models.DateField(blank=True, default=None)),
                ('slot_start_time', models.TimeField(blank=True, default=None)),
                ('slot_end_time', models.TimeField(blank=True, default=None)),
                ('is_booked', models.BooleanField(default=False)),
                ('cust', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='CustomerSlots', to=settings.AUTH_USER_MODEL)),
                ('doc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='DoctorSlots', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
