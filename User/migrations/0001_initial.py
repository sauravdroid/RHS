# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-05 05:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Snippets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2017, 6, 5, 5, 21, 19, 555156, tzinfo=utc))),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('language', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
    ]
