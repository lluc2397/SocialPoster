import sys 
import random

try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()

class TitlesManager(models.Manager):

    @property
    def random_title(self):
        titles = [al_title for al_title in self.all()]
        return random.choice(titles)


class EmojiManager(models.Manager):

    @property
    def random_emojis(self):
        emojis = [emoji for emoji in self.all()]
        return emojis


class HashtagsManager(models.Manager):

    @property
    def random_ig_hashtags(self):
        hashtags = [hashtag for hashtag in self.filter(for_ig = True)]
        return hashtags
    
    @property
    def random_tw_hashtags(self):
        hashtags = [hashtag for hashtag in self.filter(for_tw = True)]
        return hashtags
    
    @property
    def random_fb_hashtags(self):
        hashtags = [hashtag for hashtag in self.filter(for_fb = True)]
        return hashtags
    
    @property
    def random_yb_hashtags(self):
        hashtags = [hashtag for hashtag in self.filter(for_yb = True)]
        return hashtags


class ContentManager(models.Manager):
    
    @property
    def available_video(self):
        content = self.filter(published = False, has_consistent_error= False, is_video = True)
        return content[0]
    
    @property
    def available_image_for_short(self):
        content = self.filter(published = True, has_consistent_error= False, is_img = True, reusable = True, reused = False)
        return content[0]

class FoldersManager(models.Manager):

    @property
    def shorts_folder(self):
        return self.get(name = 'shorts')
    
    @property
    def logos_folder(self):
        return self.get(name = 'logos')
    
    @property
    def frases_folder(self):
        return self.get(name = 'frases')
    
    @property
    def longs_folder(self):
        return self.get(name = 'youtube videos')
    
    @property
    def resized_folder(self):
        return self.get(name = 'resized images')
    
    @property
    def audio_folder(self):
        return self.get(name = 'audio')
    
    