# Generated by Django 4.0.1 on 2022-02-17 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0010_rename_title_facebookpostrecord_default_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookpostrecord',
            name='custom_title',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='instagrampostrecord',
            name='custom_title',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='twitterpostrecord',
            name='custom_title',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='youtubepostrecord',
            name='custom_title',
            field=models.TextField(default=''),
        ),
    ]