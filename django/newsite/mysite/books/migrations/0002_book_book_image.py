# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-13 22:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_image',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]