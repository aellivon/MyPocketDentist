# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-12 09:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rules', '0006_rule_conjuction_or_disjunction_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rule',
            name='Conjuction_or_Disjunction_Order',
        ),
        migrations.AddField(
            model_name='rule',
            name='Condition_Order',
            field=models.CharField(default='', help_text='If two or more evidence exists, This field will be the basis of the  ', max_length=500),
        ),
    ]