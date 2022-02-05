from numpy import random
import requests
import sys
import logging
import datetime
from settings import Motdepasse

from modelos.models import HASHTAGS, DEFAULT_TITLES

horizontal_video_string = 'horizontal-final.mp4'

FACEBOOK_MAIN_URL = 'https://graph.facebook.com/'

# old_faceboo_page_id = '107326904530301'
# app_id = '607951806946136'
# new_facebook_page_id = '105836681984738'

logger = logging.getLogger('longs')

class FACEBOOK():
    def __init__(self, user_token='', 
    app_id = '', app_secret=Motdepasse().get_keys('FACEBOOK_APP_SECRET'), 
    long_lived_user_token=Motdepasse().get_keys('FB_USER_ACCESS_TOKEN'), 
    page_access_token='', 
    page_id=''):

        self.page_id = page_id
        self.user_token = user_token
        self.app_id = app_id
        self.app_secret = app_secret
        self.long_lived_user_token = long_lived_user_token
        self.page_access_token = page_access_token
        self.facebook_url = FACEBOOK_MAIN_URL
        self.facebook_video_url = "https://graph-video.facebook.com/"
    
    def get_long_live_user_token(self):
        url = f'{self.facebook_url}oauth/access_token'

        parameters = {
            'grant_type':'fb_exchange_token',
            'client_id' : self.app_id,
            'client_secret' : self.app_secret,
            'fb_exchange_token' : self.user_token
        }

        re = requests.get(url, params=parameters)

        if re.status_code == 200:
            token = str(re.json()['access_token'])
            Motdepasse().change_key_value('FB_USER_ACCESS_TOKEN', token)
            return token
    

    def get_long_live_page_token(self, old=False):
        url = f'{self.facebook_url}{self.page_id}'

        parameters = {
            'fields':'access_token',
            'access_token' : self.long_lived_user_token
        }

        re = requests.get(url, params=parameters)

        if re.status_code == 200:
            token = str(re.json()['access_token'])
            if old is False:
                Motdepasse().change_key_value('NEW_FB_PAGE_ACCESS_TOKEN', token)
            else:
                Motdepasse().change_key_value('OLD_FB_PAGE_ACCESS_TOKEN', token)
            return token

    
    def post_fb_video(self, description= "" ,video_url= "", title= "", post_time='',hashtags=[], post_now = False):
        """
        Post_now is False if the post has to be scheduled, True to post it now
        """
        if description == '':
            description = self.create_fb_description(hashtags)
        
        if title == '':
            title = random.choice([def_title.title for def_title in DEFAULT_TITLES.objects.all()])

        files = {'source': open(video_url, 'rb')}

        if post_now is True:
            data ={
                'access_token': self.page_access_token,
                'title':title,
                'description': description
            }

        else:
            data ={
                'access_token': self.page_access_token,
                'published' : False,
                'scheduled_publish_time': post_time,
                'title': title,
                'description': description
            }

        return self.post_content('video', data, files)

    
    def post_text(self, text= "", post_time= "", post_now = True, link=''):

        if post_now is False:
            pass
        else:
            data ={
                'access_token': self.page_access_token,
                'message': text
            }
        
        if link !='':
            data['link'] = link

        return self.post_content('text', data)



    def post_image(self, description= "", photo_url= "", title= "", post_time=datetime.datetime.now(), post_now = False):
        data ={
            'access_token': self.page_access_token,
            'url': photo_url
        }
        return self.post_content('image', data)
        
    

    def post_content(self, type:str, content, files = None):
        print ("Posting file...")
        if type == 'video':
            re = requests.post(f'{self.facebook_video_url}{self.page_id}/videos',files=files, data = content)
        if type == 'text':
            re = requests.post(f'{self.facebook_url}{self.page_id}/feed', data = content)
        if type == 'image':
            re = requests.post(f'{self.facebook_url}{self.page_id}/photos', data = content)        
        
        response = {}
        if re.status_code == 200:
            response['status'] = re.status_code
            response['post_id'] = str(re.json()['id'])            
            return response
        
        elif re.json()['error']['code'] == 190:
            logger.error('Need new user token')
            
            sys.exit()
    

    def share_post_to_old_page(self, yb_title, post_id):
        url_to_share = f'https://www.facebook.com/InversionesyFinanzas/posts/{post_id}&show_text=true'
        self.post_text(text=f'No te pierdas el nuevo video {yb_title}', link = url_to_share)
    


    

    # def schedule_video_posts_on_facebook(self, year, month, day, hour, number_to_post):
    #     folders = [folder for folder in os.listdir(to_post_dir)]

    #     for folder in folders[:number_to_post]:
    #         complete_url_folder = f'{to_post_dir}{folder}'        

    #         horizontal_url = f'{complete_url_folder}/{horizontal_video_string}'

    #         hour += random.randrange(6, 9)
    #         minute = random.randrange(0, 59)
    #         if hour >= 24:
    #             hour = 0
    #             day += 1
    #         if day >=31:
    #             day = 1
    #             month += 1
    #         if month >= 13:
    #             month = 1
    #             year += 1
        
    #         fb_desc = self.create_fb_description()
    #         fb_title = random.choice(frases_para_descripcion)
    #         fb_date = datetime.datetime(year, month, day,hour,minute).timestamp()

    #         fb_post = self.post_fb_video(
    #             description = fb_desc,
    #             video_url= horizontal_url,
    #             title=fb_title,
    #             post_time = int(fb_date)
    #         )

    #         if fb_post['status'] == 200:
    #             shutil.move(complete_url_folder, posted_dir+folder)
    #             fb_id = fb_post['vid_id']
    #             desktop_notification('Facebook', f"Video id {fb_id} was successfully uploaded.")
                

    #         else:
    #             desktop_notification('Facebook', f"Error con el post {complete_url_folder}")
    


    def create_fb_description(self, hashtags):
        hashtags = ' '.join(hashtags)
        face_description = f"""
        Prueba las herramientas que todo inversor inteligente necesita: https://inversionesyfinanzas.xyz

        Visita nuestras redes sociales:
        Facebook: https://www.facebook.com/InversionesyFinanzas/
        Instagram: https://www.instagram.com/inversiones.finanzas/
        TikTok: https://www.tiktok.com/@inversionesyfinanzas?
        Twitter : https://twitter.com/InvFinz
        LinkedIn : https://www.linkedin.com/company/inversiones-finanzas

        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        {hashtags}
        """
        return face_description




            




