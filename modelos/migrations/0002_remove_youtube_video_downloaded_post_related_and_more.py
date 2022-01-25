# Generated by Django 4.0.1 on 2022-01-25 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youtube_video_downloaded',
            name='post_related',
        ),
        migrations.AddField(
            model_name='youtube_video_downloaded',
            name='content_related',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.local_content'),
        ),
    ]
