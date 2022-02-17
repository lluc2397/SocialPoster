import sys 
import random
import uuid

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

    def random_emojis(self, num):        
        emojis = []
        for i in range(num):
            emojis.append(self.get(id = random.randint(1,self.all().count())))
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

    def create_uuid(self) -> uuid:
        new_iden = uuid.uuid4()
        if self.filter(iden = new_iden).exists():
            return self.create_uuid()
        else:
            return new_iden
    
    @property
    def available_video(self):
        content = self.filter(
            published = False,
            has_consistent_error= False,
            is_video = True,
            reused = False,
            reusable = False)
        return content[0]
    
    @property
    def available_downloaded_video(self):
        return self.available_video.video_downloaded.all()[0]
    
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


class YoutubeVideoDowloadedManager(models.Manager):

    @property
    def video_downloaded(self):
        return self.filter(downloaded = True, captions_downloaded=True)[0]