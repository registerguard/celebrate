# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-19 01:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20170109_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerguardmemoryimage',
            name='image',
            field=models.ImageField(blank=True, upload_to='/rginfo/oper/celebrate/media/celebrate_images'),
        ),
    ]
