# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
