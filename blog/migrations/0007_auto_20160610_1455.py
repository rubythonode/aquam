# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-10 05:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20160610_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorys',
            name='gallery',
        ),
        migrations.AddField(
            model_name='gallery',
            name='categorys',
            field=models.ManyToManyField(to='blog.Categorys'),
        ),
    ]
