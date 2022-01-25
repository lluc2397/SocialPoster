# Generated by Django 4.0.1 on 2022-01-25 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DEFAULT_TITLES',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='EMOJIS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emoji', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='FOLDERS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_path', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='HASHTAGS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='')),
                ('is_trending', models.BooleanField(default=False)),
                ('for_fb', models.BooleanField(default=False)),
                ('for_ig', models.BooleanField(default=False)),
                ('for_tw', models.BooleanField(default=False)),
                ('for_yb', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LOCAL_CONTENT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iden', models.UUIDField(null=True, unique=True)),
                ('published', models.BooleanField(default=False)),
                ('main_folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.folders')),
            ],
        ),
        migrations.CreateModel(
            name='YOUTUBE_CHANNELS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='')),
                ('url', models.TextField(default='')),
                ('all_parsed', models.BooleanField(default=False)),
                ('keep_scraping', models.BooleanField(default=False)),
                ('last_time_parsed', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='YOUTUBE_POST',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_local', models.BooleanField(default=True)),
                ('post_type', models.IntegerField(blank=True, choices=[(1, 'Video'), (2, 'Short')], null=True)),
                ('is_original', models.BooleanField(default=False)),
                ('date_posted', models.DateTimeField(auto_now_add=True, null=True)),
                ('title', models.TextField(default='', null=True)),
                ('caption', models.TextField(default='\n\nPrueba las herramientas que todo inversor inteligente necesita: https://inversionesyfinanzas.xyz\n\nVisita nuestras redes sociales:\nFacebook: https://www.facebook.com/InversionesyFinanzas/\nInstagram: https://www.instagram.com/inversiones.finanzas/\nTikTok: https://www.tiktok.com/@inversionesyfinanzas?\nTwitter : https://twitter.com/InvFinz\nLinkedIn : https://www.linkedin.com/company/inversiones-finanzas\n\nEn este canal de INVERSIONES & FINANZAS, aprende cómo realizar un BUEN ANÁLISIS de las EMPRESAS. Descubre dónde invertir y de qué forma ENCONTRAR BUENAS OPORTUNIDADES de INVERSIÓN.\n\nAPRENDE como invertir en la bolsa de valores.🥇 DESCUBRE las mejores ESTRATEGIAS que existen para INVERTIR y los pasos que deberías seguir para INVERTIR en la BOLSA mexicana de VALORES. ¿Quieres CONOCER la forma de INVERTIR de los INVERSORES más célebres de forma clara y FÁCIL? ADÉNTRATE en el ASOMBROSO mundo de las INVERSIONES. Si lo  que buscas es aprender a : \ninvertir en la bolsa de valores\ninvertir sin dinero\ninvertir con poco dinero\ninvertir siendo joven\nmultiplicar tu dinero\nanalizar una empresa\n')),
                ('social_id', models.TextField(default='')),
                ('content_related', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.local_content')),
                ('default_title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.default_titles')),
                ('emojis', models.ManyToManyField(blank=True, to='modelos.EMOJIS')),
                ('hashtags', models.ManyToManyField(blank=True, to='modelos.HASHTAGS')),
            ],
        ),
        migrations.CreateModel(
            name='YOUTUBE_VIDEO_DOWNLOADED',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField(default='', unique=True)),
                ('old_title', models.TextField(default='')),
                ('new_title', models.TextField(default='')),
                ('downloaded', models.BooleanField(default=False)),
                ('has_caption', models.BooleanField(default=False)),
                ('download_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('original_channel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.youtube_channels')),
                ('post_related', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.youtube_post')),
            ],
        ),
        migrations.CreateModel(
            name='TWITTER_POST',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_local', models.BooleanField(default=True)),
                ('post_type', models.IntegerField(blank=True, choices=[(1, 'Video'), (2, 'Image'), (3, 'Text'), (4, 'Repost'), (5, 'Text and video'), (6, 'Text and image')], null=True)),
                ('is_original', models.BooleanField(default=False)),
                ('date_posted', models.DateTimeField(auto_now_add=True, null=True)),
                ('caption', models.TextField(default='')),
                ('social_id', models.TextField(default='')),
                ('content_related', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.local_content')),
                ('emojis', models.ManyToManyField(blank=True, to='modelos.EMOJIS')),
                ('hashtags', models.ManyToManyField(blank=True, to='modelos.HASHTAGS')),
            ],
        ),
        migrations.CreateModel(
            name='INSTAGRAM_POST',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_local', models.BooleanField(default=True)),
                ('post_type', models.IntegerField(blank=True, choices=[(1, 'Video'), (2, 'Image')], null=True)),
                ('is_original', models.BooleanField(default=False)),
                ('date_posted', models.DateTimeField(auto_now_add=True, null=True)),
                ('caption', models.TextField(default='')),
                ('social_id', models.TextField(default='')),
                ('content_related', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.local_content')),
                ('emojis', models.ManyToManyField(blank=True, to='modelos.EMOJIS')),
                ('hashtags', models.ManyToManyField(blank=True, to='modelos.HASHTAGS')),
                ('title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.default_titles')),
            ],
        ),
        migrations.CreateModel(
            name='FACEBOOK_POST',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_local', models.BooleanField(default=True)),
                ('post_type', models.IntegerField(blank=True, choices=[(1, 'Video'), (2, 'Image'), (3, 'Text'), (4, 'Repost'), (5, 'Text and video'), (6, 'Text and image'), (7, 'Shorts')], null=True)),
                ('is_original', models.BooleanField(default=False)),
                ('date_posted', models.DateTimeField(auto_now_add=True, null=True)),
                ('caption', models.TextField(default='')),
                ('social_id', models.TextField(default='')),
                ('content_related', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.local_content')),
                ('emojis', models.ManyToManyField(blank=True, to='modelos.EMOJIS')),
                ('hashtags', models.ManyToManyField(blank=True, to='modelos.HASHTAGS')),
                ('title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelos.default_titles')),
            ],
        ),
    ]
