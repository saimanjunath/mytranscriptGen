# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcriptG', '0014_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='hello',
        ),
        migrations.AlterField(
            model_name='student',
            name='emailid',
            field=models.EmailField(max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='firstname',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='lastname',
            field=models.CharField(max_length=50),
        ),
    ]
