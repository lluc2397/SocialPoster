# Generated by Django 4.0.1 on 2022-01-21 17:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0003_local_content_published_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtube_channels',
            name='last_time_parsed',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 21, 17, 43, 11, 271075)),
        ),
    ]