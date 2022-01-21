import sys
import uuid

try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()

class HASHTAGS(models.Model):        
    name = models.TextField(default='')
    is_trending = models.BooleanField(default=False)
    for_fb = models.BooleanField(default=False)
    for_ig = models.BooleanField(default=False)
    for_tw = models.BooleanField(default=False)


class EMOJIS(models.Model):
    emoji= models.TextField(default='')


class DEFAULT_TITLES(models.Model):
    title = models.TextField(default='')

class FOLDERS(models.Model):
    full_path = models.TextField(default='')


class LOCAL_CONTENT(models.Model):
    iden = models.UUIDField(null = True, unique=True)
    main_folder = models.ForeignKey(FOLDERS, null = True, blank=True, on_delete=models.SET_NULL)


class POST(models.Model):    
    POST_TYPE = ((1, 'Video'), (2, 'Image'), (3, 'Text'), (4, 'Repost'))

    is_local = models.BooleanField(default=True)
    content_related = models.ForeignKey(LOCAL_CONTENT, null = True, blank=True, on_delete=models.SET_NULL)
    post_type = models.IntegerField(null=True, blank=True,choices=POST_TYPE)    
    is_original = models.BooleanField(default=False)    
    date_posted = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(DEFAULT_TITLES,null = True, blank=True, on_delete=models.SET_NULL)
    hashtags = models.ManyToManyField(HASHTAGS, blank=True)
    emojis = models.ManyToManyField(EMOJIS, blank=True)
    caption = models.TextField(default='')


class FACEBOOK_POST(models.Model):
    post_related = models.ForeignKey(POST, null = True, blank=True, on_delete=models.SET_NULL)    

class INSTAGRAM_POST(models.Model):
    post_related = models.ForeignKey(POST, null = True, blank=True, on_delete=models.SET_NULL)

class TWITTER_POST(models.Model):
    post_related = models.ForeignKey(POST, null = True, blank=True, on_delete=models.SET_NULL)    

class YOUTUBE_POST(models.Model):   
    post_related = models.ForeignKey(POST, null = True, blank=True, on_delete=models.SET_NULL)
    

class YOUTUBE_VIDEO_DOWNLOADED(models.Model):
    url = models.TextField(default='')
    old_title = models.TextField(default='')
    new_title = models.TextField(default='')
    original_channel = models.TextField(default='')
    downloaded = models.BooleanField(default=False)
    has_caption = models.BooleanField(default=False)
    download_date = models.DateTimeField(auto_now_add=True)
    post_related = models.ForeignKey(YOUTUBE_POST, null = True, blank=True, on_delete=models.SET_NULL)