import os
import cloudinary
import random
import time
import logging
import sys
import shutil

from editing import resize_image, create_short_from_image
from settings import Motdepasse, print_progress_bar
from modelos.models import (
    Folder,
    LocalContent,
    DefaultTilte,
    YoutubeVideoDowloaded
    )

# year = 2022
# month = 1
# day = datetime.datetime.now().day
# hour = 17

logger = logging.getLogger('longs')

cloudinary.config( 
  cloud_name = "inversionesfinanzas", 
  api_key = Motdepasse().get_keys('CLOUDINARY_API_KEY'), 
  api_secret = Motdepasse().get_keys('CLOUDINARY_SECRET'),
  secure = True
)


class Multipostage:
    def __init__(self) -> None:
        from socialmedias.facepy import Facebook
        from socialmedias.instapy import Instagram
        from socialmedias.youpy import Youtube
        from socialmedias.tweetpy import Twitter

        old_fb_page_access_token = Motdepasse().get_keys('OLD_FB_PAGE_ACCESS_TOKEN')
        new_long_live_page_token = Motdepasse().get_keys('NEW_FB_PAGE_ACCESS_TOKEN')

        old_faceboo_page_id = '107326904530301'
        new_facebook_page_id = '105836681984738'
        ig_account_id = '17841444650537865'

        self.new_facebook = Facebook(page_access_token=new_long_live_page_token, page_id=new_facebook_page_id)
        self.old_facebook = Facebook(page_access_token=old_fb_page_access_token, page_id=old_faceboo_page_id)
        self.insta = Instagram(page_access_token=new_long_live_page_token, ig_account_id=ig_account_id)
        self.youtube = Youtube()
        self.twitter = Twitter()

    def tests(self):
        video = LocalContent.objects.available_downloaded_video
        print(video)


    def delete_non_saved_local(safe):
        videos = os.listdir(Folder.objects.longs_folder.full_path)        
        for video in videos:
            existe = LocalContent.objects.filter(iden=video)
            if existe.count() == 0:
                shutil.rmtree(Folder.objects.longs_folder.full_path + video)


    def download_captions(self):
        videos = YoutubeVideoDowloaded.objects.filter(downloaded = True, captions_downloaded=False)
        total = videos.count()
        for i, video in enumerate(videos):
            print_progress_bar(i,total,f'Total: {total}')
            if video.content_related is None:
                video.downloaded = False
                video.save()
                continue
            captions_response = self.youtube.get_caption(video.content_related, video)

            if captions_response['result'] == 'error':
                video.content_related.has_consistent_error = True
                video.content_related.error_msg = captions_response['message']
                video.content_related.save()
                continue
        logger.info('Captions donwloaded done')


    def share_long(self, retry=0):
        retry = retry
        video = LocalContent.objects.available_downloaded_video

        logger.info(f'Starting the uploading process')
        
        yb_response = self.youtube.upload_default_english_long_video(video)

        if yb_response['result'] == 'error':            
            retry += 1
            if retry == 5:
                logger.info(f'Error with the following video --> {video.id}')
                sys.exit()
            logger.info(f'Error with the following video --> {video.id}, starting again with an other')
            return self.share_long(retry)
        
        custom_title = video.old_title
        if video.new_title:
            custom_title = video.new_title
            
        logger.info(f'Starting the repost process of {custom_title} in 1 min')
        time.sleep(60)
        repost_response = self.repost_youtube_video(custom_title, yb_response['extra'])

        return repost_response
        

    def repost_youtube_video(self, yb_title, yb_video_id):
        url_to_share = f'https://www.youtube.com/watch?v={yb_video_id}'
        default_title = DefaultTilte.objects.random_title

        fb_title = f"""{default_title.title}
        {yb_title}"""

        tw_status = f"""{fb_title}
        {url_to_share}
        """       

        tweeter_post_id = self.twitter.tweet_text(tw_status)

        fb_post_id =  self.new_facebook.post_text(text=fb_title, link = url_to_share)

        fb_post_id_repost = fb_post_id['post_id'].split('_')[1]

        self.old_facebook.share_facebook_post(post_id = fb_post_id_repost, yb_title = yb_title)

        
    

    def create_post_image(self):
        name,top,bottom = 'frases', 0, 122
        if random.randint(1,2) == 1:
            name,top,bottom = 'logos', 58, 5
        
        original_folder = Folder.objects.get(name = name)
        images_av = os.listdir(original_folder.full_path)[0]

        image_path = f'{original_folder.full_path}{images_av}'
        if image_path.endswith('.jpg') is False:
            image_path = f'{image_path}/{images_av}.jpg'

        final_folder = Folder.objects.resized_folder

        local_content = LocalContent.objects.create(
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
        carpeta = Folder.objects.shorts_folder

        local_content = LocalContent.objects.available_image_for_short        

        new_content = LocalContent.objects.create(
            main_folder = carpeta,
            is_video = True,
            reused = True,
            original_local = local_content.iden,
        )
        
        
        image = local_content.local_resized_image_path
        new_dir = new_content.create_dir()
        
        fps_and_duration = random.randint(25, 33)
        
        create_short_from_image(new_dir, image, fps_and_duration)
        
        yb_post_result = self.youtube.upload_post_youtube_short(new_content)

        if yb_post_result != 'error-uploading-video':
            self.repost_youtube_video(' ', yb_post_result, frase_default='')
        
        insta_post_result = self.insta.default_post_on_instagram(local_content, post_type=1)
        
        return insta_post_result
        
