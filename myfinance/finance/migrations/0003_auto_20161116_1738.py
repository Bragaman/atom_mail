# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-16 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_auto_20161116_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(default='empty account name', max_length=32),
        ),
        migrations.AlterField(
            model_name='account',
            name='number',
            field=models.CharField(max_length=32),
        ),
    ]