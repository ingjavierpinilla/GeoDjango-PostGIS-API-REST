# Generated by Django 3.1.6 on 2021-02-01 16:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 1, 16, 2, 48, 685488, tzinfo=utc)),
        ),
    ]
