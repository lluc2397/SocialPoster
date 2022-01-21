
import subprocess as s
import os
import json
import cloudinary
import random

from editing import create_img_from_frame

from modelos import (
    EMOJIS,
    DEFAULT_TITLES,
    POSTS,
    VIDEOS_TO_PARSE,
    HASHTAGS
)

ig_account_id = '17841444650537865'

# year = 2022
# month = 1
# day = datetime.datetime.now().day
# hour = 17


audio_directory = "/home/lucas/smcontent/musicfiles/"

to_post_dir = '/home/lucas/smcontent/por_publicar/'

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

        self.facebook = FACEBOOK
        self.insta = INSTAGRAM
        self.youtube = YOUTUBE
    
    def post_shorts(self):
        
        short_video_path= random.choice(os.listdir(to_post_dir))            
        short_url = short_video_path + vertical_video_string

        self.facebook(page_access_token = new_long_live_page_token).post_fb_video(video_url=short_url, post_now = True)
        
        ig_image = create_img_from_frame(short_video_path + horizontal_video_string)
        self.insta(page_access_token = new_long_live_page_token).post_ig(image_url=ig_image)

        self.youtube().initialize_upload(video_file=short_url, privacyStatus = 'public')
        #post on fb
        #psot on tw
        #post on ig
        #post on yb
        pass
    

    def crosspostage(self):
        #post yb and return id
        #share on fb
        #share on tw
        pass

