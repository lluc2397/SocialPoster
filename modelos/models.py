import os
import sys
import logging

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
    FoldersManager,
    YoutubeVideoDowloadedManager,
    GeneralManager
)

logger = logging.getLogger('longs')

class Hashtag(models.Model):        
    name = models.TextField(default='')
    is_trending = models.BooleanField(default=False)
    for_fb = models.BooleanField(default=False)
    for_ig = models.BooleanField(default=False)
    for_tw = models.BooleanField(default=False)
    for_yb = models.BooleanField(default=False)
    objects = HashtagsManager()

    def __str__(self) -> str:
        return str(self.name)


class Emoji(models.Model):
    emoji= models.TextField(default='')
    objects = EmojiManager()

    def __str__(self) -> str:
        return str(self.emoji)


class DefaultTilte(models.Model):
    title = models.TextField(default='')
    objects = TitlesManager()

    def __str__(self) -> str:
        return str(self.title)    
    

class Folder(models.Model):
    name = models.CharField(max_length=1000,default='')
    full_path = models.TextField(default='')
    objects = FoldersManager()

    def __str__(self) -> str:
        return str(self.full_path)
    
    def save(self, *args, **kwargs):
        if self.full_path.endswith('/') is False:
            self.full_path = self.full_path + '/'
        return super().save(*args, **kwargs)


class LocalContent(models.Model):
    iden = models.UUIDField(null = True, unique=True)
    main_folder = models.ForeignKey(Folder, null = True, blank=True, on_delete=models.SET_NULL)
    published = models.BooleanField(default=False)
    is_video = models.BooleanField(default=True)
    is_img = models.BooleanField(default=False)
    is_short = models.BooleanField(default=False)
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
            self.iden = LocalContent.objects.create_uuid()
        return super().save(*args, **kwargs)
    
    @property
    def local_path(self):
        return f'{self.main_folder.full_path}{self.iden}/'

    @property
    def local_resized_image_path(self):
        return f'{self.local_path}resized-image.jpg'
    
    @property
    def local_vertical_short_path(self):
        return f'{self.local_path}vertical-final.mp4'

    @property
    def local_horizontal_short_path(self):
        return f'{self.local_path}horizontal-final.mp4'
    
    def create_dir(self):
        os.mkdir(self.local_path)
        return str(self.local_path)



class PostRecord(models.Model):
    POST_TYPE = None

    is_local = models.BooleanField(default=True)
    content_related = models.ForeignKey(LocalContent, null = True, blank=True, on_delete=models.SET_NULL)
    post_type = models.IntegerField(null=True, blank=True,choices=POST_TYPE)    
    is_original = models.BooleanField(default=False)    
    date_posted = models.DateTimeField(auto_now_add=True, null = True)
    default_title = models.ForeignKey(DefaultTilte,null = True, blank=True, on_delete=models.SET_NULL)
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    emojis = models.ManyToManyField(Emoji, blank=True)
    caption = models.TextField(default='')
    social_id = models.TextField(default='')
    use_default_title = models.BooleanField(default=True)
    custom_title = models.TextField(default='')
    objects = models.Manager()
    general_manager = GeneralManager()

    class Meta:
        abstract = True
    
    def __str__(self) -> str:
        return str(self.id)

class FacebookPostRecord(PostRecord):
    POST_TYPE = ((1, 'Video'), (2, 'Image'), (3, 'Text'),
    (4, 'Repost'), (5, 'Text and video'), (6, 'Text and image'), (7, 'Shorts'))


class InstagramPostRecord(PostRecord):
    POST_TYPE = ((1, 'Video'), (2, 'Image'))


class TwitterPostRecord(PostRecord):
    POST_TYPE = ((1, 'Video'), (2, 'Image'), (3, 'Text'), 
    (4, 'Repost'), (5, 'Text and video'), (6, 'Text and image'))


class YoutubePostRecord(PostRecord):   
    POST_TYPE = ((1, 'Video'), (2, 'Short'))


class YoutubeChannel(models.Model):
    name = models.TextField(default='')
    url = models.TextField(default='')
    all_parsed = models.BooleanField(default=False)
    keep_scraping = models.BooleanField(default=False)
    last_time_parsed = models.DateTimeField(auto_now_add=True, null = True)

    def __str__(self) -> str:
        return str(self.name)


class YoutubeVideoDowloaded(models.Model):
    url = models.TextField(default='', unique=True)
    old_title = models.TextField(default='')
    new_title = models.TextField(default='')
    original_channel = models.ForeignKey(YoutubeChannel, null = True, blank=True, on_delete=models.SET_NULL)
    downloaded = models.BooleanField(default=False)
    has_caption = models.BooleanField(default=False)
    captions_downloaded = models.BooleanField(default=False)
    download_date = models.DateTimeField(auto_now_add=True, null = True)
    content_related = models.ForeignKey(LocalContent, null = True, blank=True, on_delete=models.CASCADE, related_name = 'video_downloaded')
    objects = YoutubeVideoDowloadedManager()

    def __str__(self) -> str:
        return str(self.old_title)