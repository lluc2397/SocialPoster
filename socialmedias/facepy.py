from numpy import random
import requests
import datetime

from modelos.models import HASHTAGS, DEFAULT_TITLES

horizontal_video_string = 'horizontal-final.mp4'

FACEBOOK_MAIN_URL = 'https://graph.facebook.com/'


class FACEBOOK():
    def __init__(self, user_token='', page_access_token='', page_id=''):
        self.page_id = page_id
        self.user_token = user_token
        self.page_access_token = page_access_token
        self.facebook_url = FACEBOOK_MAIN_URL
        self.facebook_video_url = "https://graph-video.facebook.com/"
    
    def get_long_live_user_token(self, app_id, app_secret):
        url = f'{self.facebook_url}oauth/access_token'

        parameters = {
            'grant_type':'fb_exchange_token',
            'client_id' : app_id,
            'client_secret' : app_secret,
            'fb_exchange_token' : self.user_token
        }

        re = requests.get(url, params=parameters)

        if re.status_code == 200:
            token = str(re.json()['access_token'])
            print(token)
    
    
    

    def get_long_live_page_token(self):
        url = f'{self.facebook_url}{self.page_id}'

        parameters = {
            'fields':'access_token',
            'access_token' : self.user_token
        }

        re = requests.get(url, params=parameters)

        if re.status_code == 200:
            token = str(re.json()['access_token'])
            print(token)


    
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

        print ("Posting file on facebook...")
        re = requests.post(f'{self.facebook_video_url}{self.page_id}/videos',files=files, data = data)
        
        response = {}
        if re.status_code == 200:
            response['status'] = re.status_code
            response['vid_id'] = str(re.json()['id'])            
            return response

        else:
            print(re)
            print(re.content)
            print(re.json())


    
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

        print ("Posting file...")
        re = requests.post(f'{self.facebook_url}{self.page_id}/feed', data = data)

        response = {}
        if re.status_code == 200:
            response['status'] = re.status_code
            response['post_id'] = str(re.json()['id'])
            print('main response', response)       
            return response

        else:
            print(re)
            print(re.content)
            print(re.json())



    def post_image(self, description= "", photo_url= "", title= "", post_time=datetime.datetime.now(), post_now = False):
        data ={
            'access_token': self.page_access_token,
            'url': photo_url
        }
        print ("Posting file...")
        requests.post(f'{self.facebook_url}{self.page_id}/photos', data = data)
    

    def share_post_to_old_page(self, yb_title, post_id):
        print('repost')
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




            




