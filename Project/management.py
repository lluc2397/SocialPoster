
import subprocess as s
import os
import json
import uuid
import cloudinary
import random
import time
from editing import create_img_from_frame

from modelos.models import (
    EMOJIS,
    DEFAULT_TITLES,
    LOCAL_CONTENT,
    FOLDERS,
    HASHTAGS,
    FACEBOOK_POST,
    YOUTUBE_POST,
    TWITTER_POST,
    INSTAGRAM_POST,
    YOUTUBE_VIDEO_DOWNLOADED,
    youtube_description
)

ig_account_id = '17841444650537865'

# year = 2022
# month = 1
# day = datetime.datetime.now().day
# hour = 17


audio_directory = "/home/lucas/smcontent/musicfiles/"

posted_dir = '/home/lucas/smcontent/publicados/'

horizontal_video_string = 'horizontal-final.mp4'

vertical_video_string = 'vertical-final.mp4'

def get_keys(name):
    path_keys = os.path.abspath(os.path.join(os.path.dirname(__file__),'../../keys.json'))
    keys_json = open(path_keys)
    data = json.load(keys_json)
    return data[name]

def desktop_notification(title, message=''):
    s.call(['notify-send', f'{title}',f'{message}'])

cloudinary.config( 
  cloud_name = "inversionesfinanzas", 
  api_key = get_keys('CLOUDINARY_API_KEY'), 
  api_secret = get_keys('CLOUDINARY_SECRET'),
  secure = True
)

old_fb_page_access_token = get_keys('OLD_FB_PAGE_ACCESS_TOKEN')
user_access_token = get_keys('FB_USER_ACCESS_TOKEN')

old_faceboo_page_id = '107326904530301'

new_facebook_page_id = '105836681984738'

new_long_live_page_token = get_keys('NEW_FB_PAGE_ACCESS_TOKEN')



class MULTIPOSTAGE:
    def __init__(self) -> None:
        from socialmedias.facepy import FACEBOOK
        from socialmedias.instapy import INSTAGRAM
        from socialmedias.youpy import YOUTUBE
        from socialmedias.tweetpy import TWITEER

        self.facebook = FACEBOOK
        self.insta = INSTAGRAM
        self.youtube = YOUTUBE
        self.twitter = TWITEER
    
    def create_uuid(self) -> uuid:
        new_iden = uuid.uuid4()
        if LOCAL_CONTENT.objects.filter(iden = new_iden).exists():
            return self.create_uuid
        else:
            return new_iden
    
    def default_post_short(self):
        try:
            short_video_path = LOCAL_CONTENT.objects.filter(main_folder = FOLDERS.objects.get(full_path = '/home/lucas/smcontent/shorts/'), published = False)[0] #devuelve un modelo

            vertical_video_path = f'{short_video_path.main_folder.full_path}{short_video_path.iden}/{vertical_video_string}'
            horizontal_video_path = f'{short_video_path.main_folder.full_path}{short_video_path.iden}/{horizontal_video_string}'

            titles = [al_title for al_title in DEFAULT_TITLES.objects.all()]

            # num_of_emojis = random.randint(0,5)

            emojis = EMOJIS.objects.all()

            emoji1 = random.choice(emojis)
            emoji2 = random.choice(emojis)

            ig_title = random.choice(titles)
            
            fb_title = random.choice(titles)
            twitter_title = random.choice(titles)

            insta_post = INSTAGRAM_POST.objects.create(
                content_related = short_video_path,
                post_type = 2,
                title = ig_title           
            )

            face_post = FACEBOOK_POST.objects.create(
                content_related = short_video_path,
                post_type = 7,
                title = fb_title,
            )

            yb_post = YOUTUBE_POST.objects.create(
                content_related = short_video_path,
                post_type = 2,
                title = yb_title,
                
                        )

            twitter_post = TWITTER_POST.objects.create(
                content_related = short_video_path,
                post_type = 1,
                        )

            insta_post.emojis.add(emoji1)
            insta_post.emojis.add(emoji2)
            face_post.emojis.add(emoji1)
            face_post.emojis.add(emoji2)
            
            twitter_post.emojis.add(emoji1)
            twitter_post.emojis.add(emoji2)

            ig_title = f'{emoji1.emoji} {ig_title.title}{emoji2.emoji}'
            
            fb_title = f'{emoji1.emoji} {fb_title.title}{emoji2.emoji}'
            twitter_title = f'{emoji1.emoji} {twitter_title.title}{emoji2.emoji}'

            twitter_post.caption = twitter_title

            ig_hashtags = []
            
            fb_hashtags = []
            twitter_hashtags = []

            for hashtag in HASHTAGS.objects.all():
                if hashtag.for_fb is True:
                    face_post.hashtags.add(hashtag)
                    fb_hashtags.append(hashtag.name)

                if hashtag.for_ig is True:
                    insta_post.hashtags.add(hashtag)
                    ig_hashtags.append(hashtag.name)

                if hashtag.for_tw is True:
                    twitter_post.hashtags.add(hashtag)
                    twitter_hashtags.append(hashtag.name)

                    

            fb_post_id = self.facebook(user_token=user_access_token, page_access_token=new_long_live_page_token, page_id=new_facebook_page_id).post_fb_video(video_url= horizontal_video_path, title=fb_title, hashtags=fb_hashtags, post_now = True)
            face_post.social_id = fb_post_id
            
            insta_post_id = self.insta(page_access_token = new_long_live_page_token, ig_account_id=ig_account_id).default_post_on_instagram(title=ig_title, local_content=horizontal_video_path, hashtags=ig_hashtags)
            
            insta_post.social_id = insta_post_id


            
            
            

            twitter_post_id = self.twitter().tweet_with_media(horizontal_video_path, twitter_title)
            twitter_post.social_id = twitter_post_id['id']

            self.facebook(user_token=user_access_token, page_access_token=old_fb_page_access_token, page_id=old_faceboo_page_id).share_post_to_old_page(new_facebook_page_id,fb_post_id)
            
            twitter_post.save()
            yb_post.save()
            face_post.save()
            insta_post.save()

            short_video_path.published = True
            short_video_path.save()

            desktop_notification('Shorts', 'Posted successfully')
            return short_video_path
            
        except Exception as e:
            print(e)
            twitter_post.delete()
            yb_post.delete()
            face_post.delete()
            insta_post.delete()
            short_video_path.published = False
            short_video_path.save()

    

    def post_long_video_youtube(self):
        video = YOUTUBE_VIDEO_DOWNLOADED.objects.filter(downloaded = False)[0]

        new_id = self.create_uuid()
        try:
            self.youtube().download_youtube_video(new_id=new_id, video_url=video.url, get_captions = True)
        except Exception as e:
            print(e)
        video.downloaded = True

        title = video.old_title
        if video.new_title:
            title = video.new_title


        video_posted = YOUTUBE_POST.objects.create(
            content_related = LOCAL_CONTENT.objects.get(iden = new_id),
            post_type = 1,
            title = title,
            hashtags = ,
            emojis = ,
            caption = ,
            social_id = ,
        )
        video.save()
        pass
        
    

    def repost_youtube_video(self, yb_title, yb_video_id):
        time.sleep(20)        
        
        hashtags = HASHTAGS.objects.all()

        facebook_post = FACEBOOK_POST.objects.create(
            is_local = False,
            post_type = 4,
            title = yb_title)

        twitter_post = TWITTER_POST.objects.create(
            is_local = False,
            post_type = 4,
            caption = yb_title)
        
        tw_hashtags = []
        fb_hashtags = []
        
        for hashtag in hashtags:
            if hashtag.for_tw is True:
                twitter_post.hashtags.add(hashtag)
                tw_hashtags.append(hashtag)
            if hashtag.for_fb is True:
                facebook_post.hashtags.add(hashtag)
                fb_hashtags.append(hashtag)
        
        fb_post_id = self.facebook(user_token=user_access_token, page_access_token=new_long_live_page_token, page_id=new_facebook_page_id).share_youtube_video(yb_title, yb_video_id)

        self.facebook(user_token=user_access_token, page_access_token=old_fb_page_access_token, page_id=old_faceboo_page_id).share_post_to_old_page(new_facebook_page_id,yb_video_id)
        
        tweeter_post_id = self.twitter().tweet_text(yb_title,tw_hashtags)
        twitter_post.social_id = tweeter_post_id
        twitter_post.save()

        facebook_post.social_id = fb_post_id
        facebook_post.save()
        



