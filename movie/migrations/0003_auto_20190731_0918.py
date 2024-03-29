# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-07-31 09:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_movie_imdbrating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='movie',
        ),
        migrations.AddField(
            model_name='movie',
            name='imdbID',
            field=models.CharField(default=datetime.datetime(2019, 7, 31, 9, 18, 35, 186183, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='movie',
            name='casts',
        ),
        migrations.AddField(
            model_name='movie',
            name='casts',
            field=models.TextField(blank=True),
        ),
        migrations.DeleteModel(
            name='Cast',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]
