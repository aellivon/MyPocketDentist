# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-25 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Evidence', '0003_auto_20171220_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='evidence',
            name='image_name',
            field=models.ImageField(default='media/None/no-img.jpg', upload_to='media/'),
        ),
    ]
