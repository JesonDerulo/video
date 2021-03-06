# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-04 18:23
from __future__ import unicode_literals

import courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_course_secondary'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, height_field='image_height', null=True, upload_to=courses.models.handle_upload, width_field='image_width'),
        ),
        migrations.AddField(
            model_name='course',
            name='image_height',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='image_width',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
