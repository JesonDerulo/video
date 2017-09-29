# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-29 17:21
from __future__ import unicode_literals

import courses.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20170928_2120'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lecture',
            options={'ordering': ['order', 'title']},
        ),
        migrations.AddField(
            model_name='lecture',
            name='order',
            field=courses.fields.PositionField(default=-1),
        ),
    ]
