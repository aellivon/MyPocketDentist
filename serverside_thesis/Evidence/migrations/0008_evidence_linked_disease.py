# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-26 09:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Disease', '0004_disease_cause'),
        ('Evidence', '0007_auto_20180120_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='evidence',
            name='linked_disease',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='linked_disease', to='Disease.Disease'),
        ),
    ]
