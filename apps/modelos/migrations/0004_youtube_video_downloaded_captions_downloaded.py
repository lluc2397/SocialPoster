# Generated by Django 4.0.1 on 2022-01-25 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0003_twitter_post_default_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtube_video_downloaded',
            name='captions_downloaded',
            field=models.BooleanField(default=False),
        ),
    ]
