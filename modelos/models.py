import uuid
import os
import sys

try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()

from modelos.manager import (
    TitlesManager,
    HashtagsManager,
    EmojiManager,
    ContentManager,
    FoldersManager
)
youtube_description = f"""

Prueba las herramientas que todo inversor inteligente necesita: https://inversionesyfinanzas.xyz

Visita nuestras redes sociales:
Facebook: https://www.facebook.com/InversionesyFinanzas/
Instagram: https://www.instagram.com/inversiones.finanzas/
TikTok: https://www.tiktok.com/@inversionesyfinanzas?
Twitter : https://twitter.com/InvFinz
LinkedIn : https://www.linkedin.com/company/inversiones-finanzas

En este canal de INVERSIONES & FINANZAS, aprende cómo realizar un BUEN ANÁLISIS de las EMPRESAS. Descubre dónde invertir y de qué forma ENCONTRAR BUENAS OPORTUNIDADES de INVERSIÓN.

APRENDE como invertir en la bolsa de valores.🥇 DESCUBRE las mejores ESTRATEGIAS que existen para INVERTIR y los pasos que deberías seguir para INVERTIR en la BOLSA mexicana de VALORES. ¿Quieres CONOCER la forma de INVERTIR de los INVERSORES más célebres de forma clara y FÁCIL? ADÉNTRATE en el ASOMBROSO mundo de las INVERSIONES. Si lo  que buscas es aprender a : 
invertir en la bolsa de valores
invertir sin dinero
invertir con poco dinero
invertir siendo joven
multiplicar tu dinero
analizar una empresa
"""


class HASHTAGS(models.Model):        
    name = models.TextField(default='')
    is_trending = models.BooleanField(default=False)
    for_fb = models.BooleanField(default=False)
    for_ig = models.BooleanField(default=False)
    for_tw = models.BooleanField(default=False)
    for_yb = models.BooleanField(default=False)
    objects = HashtagsManager()

    def __str__(self) -> str:
        return str(self.name)


class EMOJIS(models.Model):
    emoji= models.TextField(default='')
    objects = EmojiManager()

    def __str__(self) -> str:
        return str(self.emoji)


class DEFAULT_TITLES(models.Model):
    title = models.TextField(default='')
    objects = TitlesManager()

    def __str__(self) -> str:
        return str(self.title)    
    

class FOLDERS(models.Model):
    name = models.CharField(max_length=1000,default='')
    full_path = models.TextField(default='')
    objects = FoldersManager()

    def __str__(self) -> str:
        return str(self.full_path)
    
    def save(self, *args, **kwargs):
        if self.full_path.endswith('/') is False:
            self.full_path = self.full_path + '/'
        return super().save(*args, **kwargs)


class LOCAL_CONTENT(models.Model):
    iden = models.UUIDField(null = True, unique=True)
    main_folder = models.ForeignKey(FOLDERS, null = True, blank=True, on_delete=models.SET_NULL)
    published = models.BooleanField(default=False)
    is_video = models.BooleanField(default=True)
    is_img = models.BooleanField(default=False)
    reused = models.BooleanField(default=False)
    reusable = models.BooleanField(default=False)
    original_local = models.UUIDField(null = True)
    has_consistent_error = models.BooleanField(default=False)
    error_msg = models.TextField(default='')
    objects = ContentManager()

    def __str__(self) -> str:
        return str(self.iden)
    
    def save(self, *args, **kwargs):
        if self.iden is None:
            self.iden = self.create_uuid()
        return super().save(*args, **kwargs)
    
    def create_uuid(self) -> uuid:
        new_iden = uuid.uuid4()
        if self.objects.filter(iden = new_iden).exists():
            return self.create_uuid()
        else:
            return new_iden
    
    @property
    def local_path(self):
        return f'{self.main_folder.full_path}{self.iden}/'
    
    def create_dir(self):
        os.mkdir(self.local_path)
        return str(self.local_path)


class FACEBOOK_POST(models.Model):
    POST_TYPE = ((1, 'Video'), (2, 'Image'), (3, 'Text'),
    (4, 'Repost'), (5, 'Text and video'), (6, 'Text and image'), (7, 'Shorts'))

    is_local = models.BooleanField(default=True)
    content_related = models.ForeignKey(LOCAL_CONTENT, null = True, blank=True, on_delete=models.SET_NULL)
    post_type = models.IntegerField(null=True, blank=True,choices=POST_TYPE)    
    is_original = models.BooleanField(default=False)    
    date_posted = models.DateTimeField(auto_now_add=True, null = True)
    title = models.ForeignKey(DEFAULT_TITLES,null = True, blank=True, on_delete=models.SET_NULL)
    hashtags = models.ManyToManyField(HASHTAGS, blank=True)
    emojis = models.ManyToManyField(EMOJIS, blank=True)
    caption = models.TextField(default='')
    social_id = models.TextField(default='')

    def __str__(self) -> str:
        return str(self.id)

class INSTAGRAM_POST(models.Model):
    POST_TYPE = ((1, 'Video'), (2, 'Image'))

    is_local = models.BooleanField(default=True)
    content_related = models.ForeignKey(LOCAL_CONTENT, null = True, blank=True, on_delete=models.SET_NULL)
    post_type = models.IntegerField(null=True, blank=True,choices=POST_TYPE)    
    is_original = models.BooleanField(default=False)    
    date_posted = models.DateTimeField(auto_now_add=True, null = True)
    title = models.ForeignKey(DEFAULT_TITLES,null = True, blank=True, on_delete=models.SET_NULL)
    hashtags = models.ManyToManyField(HASHTAGS, blank=True)
    emojis = models.ManyToManyField(EMOJIS, blank=True)
    caption = models.TextField(default='')
    social_id = models.TextField(default='')

    def __str__(self) -> str:
        return str(self.id)

class TWITTER_POST(models.Model):
    POST_TYPE = ((1, 'Video'), (2, 'Image'), (3, 'Text'), 
    (4, 'Repost'), (5, 'Text and video'), (6, 'Text and image'))

    is_local = models.BooleanField(default=True)
    content_related = models.ForeignKey(LOCAL_CONTENT, null = True, blank=True, on_delete=models.SET_NULL)
    post_type = models.IntegerField(null=True, blank=True,choices=POST_TYPE)    
    is_original = models.BooleanField(default=False)    
    date_posted = models.DateTimeField(auto_now_add=True, null = True)   
    default_title = models.ForeignKey(DEFAULT_TITLES,null = True, blank=True, on_delete=models.SET_NULL) 
    hashtags = models.ManyToManyField(HASHTAGS, blank=True)
    emojis = models.ManyToManyField(EMOJIS, blank=True)
    caption = models.TextField(default='')
    social_id = models.TextField(default='')

    def __str__(self) -> str:
        return str(self.id) 

class YOUTUBE_POST(models.Model):   
    POST_TYPE = ((1, 'Video'), (2, 'Short'))

    is_local = models.BooleanField(default=True)
    content_related = models.ForeignKey(LOCAL_CONTENT, null = True, blank=True, on_delete=models.SET_NULL)
    post_type = models.IntegerField(null=True, blank=True,choices=POST_TYPE)    
    is_original = models.BooleanField(default=False)    
    date_posted = models.DateTimeField(auto_now_add=True, null = True)
    default_title = models.ForeignKey(DEFAULT_TITLES,null = True, blank=True, on_delete=models.SET_NULL)
    title = models.TextField(default='',null = True)
    hashtags = models.ManyToManyField(HASHTAGS, blank=True)
    emojis = models.ManyToManyField(EMOJIS, blank=True)
    caption = models.TextField(default=youtube_description)
    social_id = models.TextField(default='')

    def __str__(self) -> str:
        return str(self.id)


class YOUTUBE_CHANNELS(models.Model):
    name = models.TextField(default='')
    url = models.TextField(default='')
    all_parsed = models.BooleanField(default=False)
    keep_scraping = models.BooleanField(default=False)
    last_time_parsed = models.DateTimeField(auto_now_add=True, null = True)

    def __str__(self) -> str:
        return str(self.name)


class YOUTUBE_VIDEO_DOWNLOADED(models.Model):
    url = models.TextField(default='', unique=True)
    old_title = models.TextField(default='')
    new_title = models.TextField(default='')
    original_channel = models.ForeignKey(YOUTUBE_CHANNELS, null = True, blank=True, on_delete=models.SET_NULL)
    downloaded = models.BooleanField(default=False)
    has_caption = models.BooleanField(default=False)
    captions_downloaded = models.BooleanField(default=False)
    download_date = models.DateTimeField(auto_now_add=True, null = True)
    content_related = models.ForeignKey(LOCAL_CONTENT, null = True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return str(self.old_title)