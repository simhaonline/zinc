# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-16 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zinc', '0004_zone_cached_ns_records'),
    ]

    operations = [
        migrations.AddField(
            model_name='policymember',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
    ]
