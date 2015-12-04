# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcriptG', '0015_auto_20151203_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='CName',
            field=models.CharField(max_length=50),
        ),
    ]
