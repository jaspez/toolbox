# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-04-28 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0002_auto_20170427_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobstatus',
            name='finish_time',
            field=models.DateTimeField(default=0, null=True),
        ),
    ]
