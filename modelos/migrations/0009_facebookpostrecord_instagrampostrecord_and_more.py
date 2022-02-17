# Generated by Django 4.0.1 on 2022-02-15 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0008_local_content_error_msg_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookPostRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_local', models.BooleanField(default=True)),
                ('post_type', models.IntegerField(blank=True, null=True)),
                ('is_original', models.BooleanField(default=False)),
                ('date_posted', models.DateTimeField(auto_now_add=True, null=True)),
                ('caption', models.TextField(default='')),
                ('social_id', models.TextField(default='')),
                ('use_default_title', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InstagramPostRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_local', models.BooleanField(default=True)),
                ('post_type', models.IntegerField(blank=True, null=True)),
                ('is_original', models.BooleanField(default=False)),
                ('date_posted', models.DateTimeField(auto_now_add=True, null=True)),
                ('caption', models.TextField(default='')),
                ('social_id', models.TextField(default='')),
                ('use_default_title', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TwitterPostRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_local', models.BooleanField(default=True)),
                ('post_type', models.IntegerField(blank=True, null=True)),
                ('is_original', models.BooleanField(default=False)),
                ('date_posted', models.DateTimeField(auto_now_add=True, null=True)),
                ('caption', models.TextField(default='')),
                ('social_id', models.TextField(default='')),
                ('use_default_title', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YoutubePostRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_local', models.BooleanField(default=True)),
                ('post_type', models.IntegerField(blank=True, null=True)),
                ('is_original', models.BooleanField(default=False)),
                ('date_posted', models.DateTimeField(auto_now_add=True, null=True)),
                ('caption', models.TextField(default='')),
                ('social_id', models.TextField(default='')),
                ('use_default_title', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='FOLDERS',
            new_name='Folder',
        ),
        migrations.RenameModel(
            old_name='YOUTUBE_CHANNELS',
            new_name='YoutubeChannel',
        ),
        migrations.RenameModel(
            old_name='YOUTUBE_VIDEO_DOWNLOADED',
            new_name='YoutubeVideoDowloaded',
        ),
        migrations.RemoveField(
            model_name='instagram_post',
            name='content_related',
        ),
        migrations.RemoveField(
            model_name='instagram_post',
            name='emojis',
        ),
        migrations.RemoveField(
            model_name='instagram_post',
            name='hashtags',
        ),
        migrations.RemoveField(
            model_name='instagram_post',
            name='title',
        ),
        migrations.RemoveField(
            model_name='twitter_post',
            name='content_related',
        ),
        migrations.RemoveField(
            model_name='twitter_post',
            name='default_title',
        ),
        migrations.RemoveField(
            model_name='twitter_post',
            name='emojis',
        ),
        migrations.RemoveField(
            model_name='twitter_post',
            name='hashtags',
        ),
        migrations.RemoveField(
            model_name='youtube_post',
            name='content_related',
        ),
        migrations.RemoveField(
            model_name='youtube_post',
            name='default_title',
        ),
        migrations.RemoveField(
            model_name='youtube_post',
            name='emojis',
        ),
        migrations.RemoveField(
            model_name='youtube_post',
            name='hashtags',
        ),
        migrations.RenameModel(
            old_name='DEFAULT_TITLES',
            new_name='DefaultTilte',
        ),
        migrations.RenameModel(
            old_name='EMOJIS',
            new_name='Emoji',
        ),
        migrations.RenameModel(
            old_name='HASHTAGS',
            new_name='Hashtag',
        ),
        migrations.RenameModel(
            old_name='LOCAL_CONTENT',
            new_name='LocalContent',
        ),
        migrations.DeleteModel(
            name='FACEBOOK_POST',
        ),
        migrations.DeleteModel(
            name='INSTAGRAM_POST',
        ),
        migrations.DeleteModel(
            name='TWITTER_POST',
        ),
        migrations.DeleteModel(
            name='YOUTUBE_POST',
        ),
        migrations.AddField(
            model_name='youtubepostrecord',
            name='content_related',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.localcontent'),
        ),
        migrations.AddField(
            model_name='youtubepostrecord',
            name='emojis',
            field=models.ManyToManyField(blank=True, to='modelos.Emoji'),
        ),
        migrations.AddField(
            model_name='youtubepostrecord',
            name='hashtags',
            field=models.ManyToManyField(blank=True, to='modelos.Hashtag'),
        ),
        migrations.AddField(
            model_name='youtubepostrecord',
            name='title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.defaulttilte'),
        ),
        migrations.AddField(
            model_name='twitterpostrecord',
            name='content_related',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.localcontent'),
        ),
        migrations.AddField(
            model_name='twitterpostrecord',
            name='emojis',
            field=models.ManyToManyField(blank=True, to='modelos.Emoji'),
        ),
        migrations.AddField(
            model_name='twitterpostrecord',
            name='hashtags',
            field=models.ManyToManyField(blank=True, to='modelos.Hashtag'),
        ),
        migrations.AddField(
            model_name='twitterpostrecord',
            name='title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.defaulttilte'),
        ),
        migrations.AddField(
            model_name='instagrampostrecord',
            name='content_related',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.localcontent'),
        ),
        migrations.AddField(
            model_name='instagrampostrecord',
            name='emojis',
            field=models.ManyToManyField(blank=True, to='modelos.Emoji'),
        ),
        migrations.AddField(
            model_name='instagrampostrecord',
            name='hashtags',
            field=models.ManyToManyField(blank=True, to='modelos.Hashtag'),
        ),
        migrations.AddField(
            model_name='instagrampostrecord',
            name='title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.defaulttilte'),
        ),
        migrations.AddField(
            model_name='facebookpostrecord',
            name='content_related',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.localcontent'),
        ),
        migrations.AddField(
            model_name='facebookpostrecord',
            name='emojis',
            field=models.ManyToManyField(blank=True, to='modelos.Emoji'),
        ),
        migrations.AddField(
            model_name='facebookpostrecord',
            name='hashtags',
            field=models.ManyToManyField(blank=True, to='modelos.Hashtag'),
        ),
        migrations.AddField(
            model_name='facebookpostrecord',
            name='title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.defaulttilte'),
        ),
    ]