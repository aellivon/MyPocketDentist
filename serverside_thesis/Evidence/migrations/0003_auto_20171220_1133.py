# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-20 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Evidence', '0002_auto_20171220_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evidence',
            name='evidence_type',
            field=models.CharField(choices=[('Cause', 'Cause'), ('Observable Evidence', 'Observable Evidence')], default='Observable Evidences', max_length=20),
        ),
    ]
