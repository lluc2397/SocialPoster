# Generated by Django 4.0.1 on 2022-01-25 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0002_remove_youtube_video_downloaded_post_related_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitter_post',
            name='default_title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.default_titles'),
        ),
    ]