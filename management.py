import os
import random
import time
import logging
import sys
import shutil

from editing import resize_image, create_short_from_image

from settings import (
    Motdepasse, 
    print_progress_bar,
    error_handling)

from modelos.models import (
    Folder,
    LocalContent,
    DefaultTilte,
    YoutubeVideoDowloaded,
    FacebookPostRecord
    )

# year = 2022
# month = 1
# day = datetime.datetime.now().day
# hour = 17

logger = logging.getLogger('longs')


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
        

        a = FacebookPostRecord.objects.get(social_id = 'abracadabra')

        print(a.delete())


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
            if yb_response['where'] == 'initialize upload youtube video' or yb_response['where'] == 'upload caption youtube video':
                error_message = yb_response['message']
                logger.error(f'Error uploading videos --> {error_message}')
                sys.exit()
            else:                
                retry += 1
                if retry == 5:
                    logger.error(f'Error with the following video --> {video.id}')
                    sys.exit()
                logger.error(f'Error with the following video --> {video.id}, starting again with an other')
                time.sleep(60)
                return self.share_long(retry)
        
        custom_title = video.old_title
        if video.new_title:
            custom_title = video.new_title
            
        logger.info(f'Starting the repost process of {custom_title} in 1 min')
        time.sleep(60)
        repost_response = self.repost_youtube_video(custom_title, yb_response['extra'])

        return repost_response
        

    def repost_youtube_video(self, yb_title, yb_video_id, retry=0, skip_twitter = False):
        url_to_share = f'https://www.youtube.com/watch?v={yb_video_id}'
        default_title = DefaultTilte.objects.random_title

        fb_title = f"""{default_title.title}
        {yb_title}"""

        tw_status = f"""{fb_title}
        {url_to_share}
        """       

        if skip_twitter is False:
            tweeter_post_response = self.twitter.tweet(
                caption = tw_status,
                has_default_title = True,
                default_title = default_title,
                post_type = 4,
            )
            if tweeter_post_response['result'] == 'error':
                retry += 1
                if retry == 5:
                    error_message = tweeter_post_response['message']
                    logger.error(f'Persistent error reposting on twitter {error_message}')
                else:
                    logger.error(f'Error reposting on twitter, starting again with an other')
                    time.sleep(60)
                    return self.repost_youtube_video(yb_title, yb_video_id, retry=retry)
            retry = 0

        fb_post_response = self.new_facebook.post_on_facebook(
            post_type = 4,
            default_title = default_title,
            custom_title = fb_title,
            caption=fb_title, 
            link = url_to_share)

        if fb_post_response['result'] == 'error':
            retry += 1
            if retry == 5 or fb_post_response['message'] == 'Need new user token':
                error_message = fb_post_response['message']
                logger.error(f'Persistent error reposting on facebook {error_message}')
            else:
                logger.error(f'Error reposting on facebook, starting again with an other')
                time.sleep(60)
                return self.repost_youtube_video(yb_title, yb_video_id, retry=retry, skip_twitter = True)
        
        if fb_post_response['result'] == 'success':
            fb_post_id_repost = fb_post_response['extra'].split('_')[1]
            self.old_facebook.share_facebook_post(post_id = fb_post_id_repost, yb_title = yb_title)

    @error_handling('prepare resized image')
    def prepare_resized_image(self, cont_type):
        """
        the images are saved in the main folder for frases, in the case of logos
        the images are in a subfolder but they share the same name as the subfolder
        so adding .jpg at the end it finds the image
        """
        
        if cont_type == 'frases':
            top, bottom = 0, 122
        if cont_type == 'logos':
            top, bottom = 58, 5
        
        original_folder = Folder.objects.get(name = cont_type)
        image_available = random.choice(os.listdir(original_folder.full_path))

        image_path = f'{original_folder.full_path}{image_available}'
        if image_path.endswith('.jpg') is False:
            image_path = f'{image_path}/{image_available}.jpg'

        local_content = LocalContent.objects.create(
            main_folder = Folder.objects.resized_folder,
            is_video = False,
            is_img = True,
            reusable = True
        )

        final_path = local_content.create_dir()

        resize_image(image_path, final_path, top, bottom, delete_old = True)

        return local_content


    def share_image(self, cont_type, resize = True, retry = 0):

        if resize is True:
            resized_image_response = self.prepare_resized_image(cont_type)
        
        if resized_image_response['result'] == 'error':
            if retry == 5:
                logger.error('Max reties to create an image')
                sys.exit()
            retry += 1
            return self.share_image(cont_type, retry=retry)
        
        local_content = resized_image_response['extra']
        self.insta.post_on_instagram(local_content)
        self.twitter.tweet(local_content)

        
        local_content.published = True
        local_content.save()
    

    @error_handling('prepare short')
    def prepare_short(self):
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

        return new_content


    def share_short(self, retry=0):

        prepare_short_response = self.prepare_short()
        
        if prepare_short_response['result'] == 'error':
            if retry == 5:
                logger.error('Max reties to create a short')
                sys.exit()
            retry += 1
            return self.share_short(retry=retry)

        local_content = prepare_short_response['extra']
        self.youtube.upload_default_short(local_content)
        self.twitter.tweet(local_content, post_type=1)
        
