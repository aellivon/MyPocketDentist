# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-20 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Disease', '0003_disease_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='disease',
            name='cause',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
