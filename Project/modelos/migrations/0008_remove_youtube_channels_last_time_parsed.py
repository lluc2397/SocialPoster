# Generated by Django 4.0.1 on 2022-01-21 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0007_alter_facebook_post_post_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youtube_channels',
            name='last_time_parsed',
        ),
    ]
