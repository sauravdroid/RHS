# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-06-07 07:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0009_auto_20170607_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippets',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 7, 7, 18, 26, 984237, tzinfo=utc)),
        ),
    ]
