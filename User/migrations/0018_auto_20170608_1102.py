# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-08 11:02
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0017_auto_20170607_1917'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorAppointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointments', models.IntegerField()),
                ('completed_appointments', models.IntegerField()),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PatientAppointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=datetime.datetime(2017, 6, 8, 11, 2, 30, 278701, tzinfo=utc))),
                ('appointment_status', models.BooleanField(default=False)),
                ('care_giver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='care_giver', to=settings.AUTH_USER_MODEL)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='currentpatientstatus',
            name='visit_date',
            field=models.DateField(default=datetime.datetime(2017, 6, 8, 11, 2, 30, 275069, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='patientdiagnosis',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 8, 11, 2, 30, 277025, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='patientmedicalstatus',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 6, 8, 11, 2, 30, 276110, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='patientmedication',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 8, 11, 2, 30, 277902, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='snippets',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 8, 11, 2, 30, 272879, tzinfo=utc)),
        ),
    ]
