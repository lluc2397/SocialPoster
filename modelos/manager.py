import sys 
import random
import uuid
import logging

try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()

logger = logging.getLogger('longs')

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
    def available_image_for_short(self):
        content = self.filter(has_consistent_error= False, is_img = True, reusable = True, reused = False)
        return random.choice([* content])


class GeneralManager(models.Manager):

    def save_record(
        self, 
        local_content, 
        post_type:int, 
        is_original:bool, 
        social_id:str, 
        emojis:list, 
        hashtags:list, 
        has_default_title:bool,
        default_title='', 
        custom_title='',
        caption = ''):
        
        try:
            modelo = self.create(
            post_type = post_type,
            is_original = is_original,
            social_id = social_id,
            use_default_title = has_default_title,
            custom_title = custom_title,
            caption = caption
            )

            if local_content is not None:
                modelo.local_content = local_content
                
            if has_default_title is True:
                modelo.default_title = default_title

            if len(emojis) != 0:
                modelo.emojis.add(*emojis)

            if len(hashtags) != 0:
                modelo.hashtags.add(*hashtags)
                
            modelo.save()

            response = {
                'result':'success',
            }

        except Exception as e:
            logger.exception(f'Error while creating post record {e}')
            response = {
                'result':'error',
                'where':'save record',
                'message':f'{e}'
            }

        return response


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
    
    @property
    def long_video_local(self):
        videos = self.longs_folder.content.filter(published = False, has_consistent_error= False, is_video = True)
        return random.choice(videos)


class YoutubeVideoDowloadedManager(models.Manager):

    @property
    def videos_downloaded(self):
        return self.filter(downloaded = True, captions_downloaded=True)