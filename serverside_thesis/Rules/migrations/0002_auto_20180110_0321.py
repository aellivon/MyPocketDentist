# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-10 03:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Evidence', '0004_evidence_image_name'),
        ('Rules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RulesEvidence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evidence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidences', to='Evidence.Evidence')),
            ],
            options={
                'verbose_name': 'RulesEvidence',
                'verbose_name_plural': 'RulesEvidences',
            },
        ),
        migrations.AlterUniqueTogether(
            name='rule',
            unique_together=set([]),
        ),
        migrations.AddField(
            model_name='rulesevidence',
            name='rule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='Rules.Rule'),
        ),
        migrations.RemoveField(
            model_name='rule',
            name='evidence',
        ),
    ]
