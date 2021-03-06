# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-12 07:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Evidence', '0004_evidence_image_name'),
        ('Rules', '0003_auto_20180110_0332'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rules_evidence',
            options={'verbose_name': 'Rules Evidence', 'verbose_name_plural': 'Rules Evidences'},
        ),
        migrations.AlterUniqueTogether(
            name='rules_evidence',
            unique_together=set([('rule', 'evidence')]),
        ),
    ]
