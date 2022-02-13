

import os
import cloudinary
import random
import time
import logging
from editing import resize_image, joint_video_audio, convert_pictures_to_video
from settings import Motdepasse

from modelos.models import (
    
    DEFAULT_TITLES,
    LOCAL_CONTENT,
    FOLDERS,
    HASHTAGS,
    FACEBOOK_POST,
    
    TWITTER_POST,
    
    YOUTUBE_VIDEO_DOWNLOADED,
    
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

logger = logging.getLogger('longs')

cloudinary.config( 
  cloud_name = "inversionesfinanzas", 
  api_key = Motdepasse().get_keys('CLOUDINARY_API_KEY'), 
  api_secret = Motdepasse().get_keys('CLOUDINARY_SECRET'),
  secure = True
)

old_fb_page_access_token = Motdepasse().get_keys('OLD_FB_PAGE_ACCESS_TOKEN')
user_access_token = Motdepasse().get_keys('FB_USER_ACCESS_TOKEN')

old_faceboo_page_id = '107326904530301'

new_facebook_page_id = '105836681984738'

new_long_live_page_token = Motdepasse().get_keys('NEW_FB_PAGE_ACCESS_TOKEN')


class MULTIPOSTAGE:
    def __init__(self) -> None:
        from socialmedias.facepy import FACEBOOK
        from socialmedias.instapy import INSTAGRAM
        from socialmedias.youpy import YOUTUBE
        from socialmedias.tweetpy import TWITEER

        self.new_facebook = FACEBOOK(user_token=user_access_token, page_access_token=new_long_live_page_token, page_id=new_facebook_page_id)
        self.old_facebook = FACEBOOK(user_token=user_access_token, page_access_token=old_fb_page_access_token, page_id=old_faceboo_page_id)
        self.insta = INSTAGRAM(user_access_token=user_access_token ,page_access_token=new_long_live_page_token, ig_account_id=ig_account_id)
        self.youtube = YOUTUBE
        self.twitter = TWITEER()
    

    def default_information(self):
        default_title = ''
        default_hashtags = []
        default_emojis = []

        default_info = {}

        return default_info
    

    def share_new_long_yb_video(self, video):

        if video is None:
            video = YOUTUBE_VIDEO_DOWNLOADED.objects.filter(downloaded = False, has_caption=True)[0]
            try:
                logger.info(f'Starting the downloading process with {video}')
                local_content_related = self.youtube().download_youtube_video(video=video, get_captions = True)
                video.downloaded = True
                video.save()
                logger.info(f'Download succesfull {local_content_related}')
            except Exception as e:
                logger.error(f'error desde managmenet al descargar {e}')
                video.downloaded = False
                video.save()
                return 'error' 
        else:
            video = video
            local_content_related = video.content_related
            if video.captions_downloaded is False:
                self.youtube().get_caption(local_content_related, video)
                
        yb_title = video.old_title
        if video.new_title:
            yb_title = video.new_title

        logger.info(f'Starting the uploading process with {yb_title}')
        yb_video_id = self.youtube().upload_and_post_video_youtube(local_content_related=local_content_related,post_type=1, yb_title=yb_title, privacyStatus='public')
        

        if yb_video_id == 'no-captions':                
            return 'error'
        
        if yb_video_id == 'error-uploading-video':                
            return 'error'

        logger.info(f'Starting the repost process with {yb_video_id}')
        logger.info('Giving time to upload the video and captions')
        time.sleep(20)
        repost = self.repost_youtube_video(yb_title, yb_video_id)

        if repost == 'success':
            return 'success'
        

    def repost_youtube_video(self, yb_title, yb_video_id, frase_default=''):
        url_to_share = f'https://www.youtube.com/watch?v={yb_video_id}'
        hashtags = HASHTAGS.objects.all()

        query_default_titles = DEFAULT_TITLES.objects
        if frase_default == '':
            all_count = query_default_titles.all().count()
            num = random.randint(1, all_count-1)
            default_title = query_default_titles.get(id = num)
        else:
            default_title = query_default_titles.get_or_create(title = frase_default)[0]


        tw_hashtags = []
        fb_hashtags = []
        
        for hashtag in hashtags:
            if hashtag.for_tw is True:                
                tw_hashtags.append(hashtag)
            if hashtag.for_fb is True:                
                fb_hashtags.append(hashtag)
        
        fb_title = f"""{default_title.title}
        {yb_title}"""
        
        logger.info('Sharing the video on facebook')
        fb_post_id = self.new_facebook.post_text(text=fb_title, link = url_to_share)
        logger.info(f'Video shared on facebook, waiting a few seconds to let it process {fb_post_id}')
        time.sleep(15)
        try:
            fb_post_id_repost = fb_post_id['post_id'].split('_')[1]
            logger.info('Sharing the post of the video on the old facebook profile')
            self.old_facebook.share_post_to_old_page(yb_title,fb_post_id_repost)
        except Exception as e:
            logger.info(e)

        facebook_post = FACEBOOK_POST.objects.create(
            is_local = False,
            title = default_title,
            post_type = 4,
            caption = yb_title)
        
        for hashtag in fb_hashtags:
            facebook_post.hashtags.add(hashtag)
        facebook_post.social_id = fb_post_id['post_id']
        facebook_post.save()
        
        logger.info('Sharing the video on twitter')

        tw_status = f"""{fb_title}
        {url_to_share}
        """
        tweeter_post_id = self.twitter.tweet_text(tw_status,tw_hashtags)
        logger.info('Post shared on twitter')

        twitter_post = TWITTER_POST.objects.create(
            is_local = False,
            default_title = default_title,
            post_type = 4,
            caption = tw_status)

        for hashtag in tw_hashtags:
            twitter_post.hashtags.add(hashtag)

        twitter_post.social_id = tweeter_post_id['id']
        twitter_post.save()

        return 'success'
    

    def create_post_image(self):
        name,top,bottom = 'frases', 0, 122
        if random.randint(1,2) == 1:
            name,top,bottom = 'logos', 58, 5
        
        original_folder = FOLDERS.objects.get(name = name)
        images_av = os.listdir(original_folder.full_path)[0]

        image_path = f'{original_folder.full_path}{images_av}'
        if image_path.endswith('.jpg') is False:
            image_path = f'{image_path}/{images_av}.jpg'

        final_folder = FOLDERS.objects.get(name = 'resized images')

        local_content = LOCAL_CONTENT.objects.create(
            main_folder = final_folder,
            is_video = False,
            is_img = True,
            reusable = True
        )

        final_path = local_content.create_dir()

        resized_image = resize_image(image_path, final_path, top, bottom, delete_old = True)
        
        self.insta.default_post_on_instagram(local_content, resized_image)
        self.twitter.default_image_tweet(local_content, resized_image)

        
        local_content.published = True
        local_content.save()
    

    def create_post_short(self):
        
        folder = '/home/lucas/InvFin/smcontent/shorts-videos/'
        carpeta = FOLDERS.objects.get_or_create(name = 'shorts',full_path = folder)[0]

        local_content = LOCAL_CONTENT.objects.filter(
            published = True,
            is_img = True,
            reusable = True)[0]
        

        new_content = LOCAL_CONTENT.objects.create(
            main_folder = carpeta,
            is_video = True,
            reused = True,
            original_local = local_content.iden,
        )
        
        
        image = local_content.local_path + 'resized-image.jpg'
        new_dir = new_content.create_dir()
        
        fps = random.randint(25, 33)
        duration = random.randint(25, 33)
        new_video = convert_pictures_to_video(new_dir, image, fps, duration)
        final_short = joint_video_audio("/home/lucas/smcontent/musicfiles/", new_video, new_dir)

        yb_video = self.youtube().upload_and_post_video_youtube(new_content,post_type=2, with_caption=False)
        self.twitter.default_short_tweet(new_content, final_short)

        return 'success'
        
        



