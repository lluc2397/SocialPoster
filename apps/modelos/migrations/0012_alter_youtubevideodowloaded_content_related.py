# Generated by Django 4.0.1 on 2022-02-17 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0011_facebookpostrecord_custom_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubevideodowloaded',
            name='content_related',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='video_downloaded', to='modelos.localcontent'),
        ),
    ]