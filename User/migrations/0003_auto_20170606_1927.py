# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-06-06 19:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_auto_20170606_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippets',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 6, 19, 27, 2, 269134, tzinfo=utc)),
        ),
    ]
