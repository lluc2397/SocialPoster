# Generated by Django 4.0.1 on 2022-02-01 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0005_folders_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='local_content',
            name='is_img',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='local_content',
            name='is_video',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='local_content',
            name='reusable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='local_content',
            name='reused',
            field=models.BooleanField(default=False),
        ),
    ]
