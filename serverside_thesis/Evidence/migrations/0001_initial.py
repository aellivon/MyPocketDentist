# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-20 07:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evidence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('question', models.CharField(max_length=500)),
                ('evidence_type', models.CharField(max_length=500)),
                ('archived', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Evidence',
                'verbose_name_plural': 'Evidences',
            },
        ),
    ]
