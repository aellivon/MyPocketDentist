# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-12 08:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Rules', '0004_auto_20180112_0736'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rules_evidence',
            unique_together=set([]),
        ),
    ]
