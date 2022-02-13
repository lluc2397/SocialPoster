import requests
import time
import os

import cloudinary.uploader

from editing import create_img_from_frame

from modelos.models import DEFAULT_TITLES,INSTAGRAM_POST,HASHTAGS

horizontal_video_string = 'horizontal-final.mp4'

FACEBOOK_MAIN_URL = 'https://graph.facebook.com/'

class INSTAGRAM():
    def __init__(self, user_access_token='' ,page_access_token='', ig_account_id=''):
        self.ig_account_id = ig_account_id
        self.page_access_token = page_access_token
        self.user_access_token = user_access_token

        self.main_instagram_url = 'https://graph.instagram.com/'

        self.ig_access_token_url = f'access_token={self.page_access_token}'    

        self.instagram_url = f'{FACEBOOK_MAIN_URL}{self.ig_account_id}/'

        self.post_url = f'{self.instagram_url}media_publish?{self.ig_access_token_url}&creation_id='
    

    def get_ig_access_token(self, app_id):
        url = f'{self.main_instagram_url}access_token'

        parameters = {
            'grant_type': 'ig_exchange_token',
            'client_secret': app_id,
            'access_token': self.user_access_token
        }

        re = requests.get(url, params=parameters)

        if re.status_code == 200:
            access_token = re.json()['access_token']

    def refresh_long_live_user_token(self):
        url = f'{self.main_instagram_url}refresh_access_token'

        parameters = {
            'grant_type': 'ig_refresh_token',
            'access_token': self.user_access_token
        }

        re = requests.get(url, params=parameters)

        if re.status_code == 200:
            access_token = re.json()['access_token']
    

    def check_post_status(self, post_id):
        extra = 'fields=status_code,status'
        status_url = f'{FACEBOOK_MAIN_URL}{post_id}?{extra}&{self.ig_access_token_url}'

        s = requests.get(status_url)
        status = s.json()
        
        return status
    
    def post_ig_image(self,caption, content_url):

        print('Uploading to cloudinary')

        uploaded_image = cloudinary.uploader.upload(content_url)

        content_file = uploaded_image['secure_url']

        cloudinary_asset_id = uploaded_image['public_id']

        data = {
            'image_url': content_file,
            'caption': caption,
            'access_token': self.page_access_token
        }

        response = {
            'data':data,
            'cloudinary_asset_id': cloudinary_asset_id,
            'cloudinary_asset_type': 'img'
        }
        return response
    


    def post_ig_video(self, caption, content_url):

        print('Uploading to cloudinary')

        uploaded_video = cloudinary.uploader.upload(content_url,resource_type = "video")

        content_file = uploaded_video['secure_url']

        cloudinary_asset_id = uploaded_video['public_id']

        data = {
            'media_type':"VIDEO",
            'video_url': content_file,
            'caption': caption,
            'access_token': self.page_access_token
        }

        response = {
            'data':data,
            'cloudinary_asset_id': cloudinary_asset_id,
            'cloudinary_asset_type': 'video'
        }
        return response
    


    def pre_post_ig(self, caption, content_url, upload_cloudinary, media_type = "VIDEO"):        

        if media_type == 'VIDEO':
            data = self.post_ig_video(caption, content_url)
         
        else:
            data = self.post_ig_image(caption, content_url)
            
        print('Posting on Instagram')
        pre_post = requests.post(f'{self.instagram_url}media', data = data['data'])

        response = {
            'ig_post_id': pre_post.json()['id'],
            'cloudinary_asset_id': data['cloudinary_asset_id'],
            'cloudinary_asset_type': data['cloudinary_asset_type']
        }

        return response
    

    def publish_content_ig(self, post_id, destroy_asset):
        ig_post_id = post_id['ig_post_id']
        try:
            re = requests.post(f'{self.post_url}{ig_post_id}')
            status = self.check_post_status(ig_post_id)

            if status['status_code'] == 'PUBLISHED':
                

                if destroy_asset is True:
                    print('Video published, destroying asset on Cloudinary')
                    
                    if post_id['cloudinary_asset_type'] == 'video':
                        cloudinary.uploader.destroy(post_id['cloudinary_asset_id'], resource_type = 'video')
                    else:
                        cloudinary.uploader.destroy(post_id['cloudinary_asset_id'])

                
                return ig_post_id
            else:
                print('el satus no es published')
        except Exception as e:
            print('error when publishing', e)
        

    def post_ig(self, caption= "", hashtags=[], video_url= "", image_url= "", upload_cloudinary = True, destroy_asset = True):
        """
        destroy_asset eliminates the previous uploaded asset to Cloudinary
        
        set upload_cloudinary to False if you upload your video from a remote server
        """

        if caption == '':
            caption = self.create_ig_caption(caption, hashtags)

        if upload_cloudinary is True:
            if image_url == "":
                post_id = self.pre_post_ig(caption, video_url, upload_cloudinary = upload_cloudinary)
            
            else:
                post_id = self.pre_post_ig(caption, image_url, media_type = 'IMAGE', upload_cloudinary = upload_cloudinary)
        
        ig_post_id = post_id['ig_post_id']

        status = self.check_post_status(ig_post_id)

        if status['status_code'] == 'EXPIRED' or status['status_code'] == 'ERROR':
            print(status)

        if status['status_code'] == 'FINISHED':
            self.publish_content_ig(post_id, destroy_asset)
            return ig_post_id

        while status['status_code'] == 'IN_PROGRESS':
            time.sleep(10)
            try:
                status = self.check_post_status(ig_post_id)

                if status['status_code'] == 'EXPIRED' or status['status_code'] == 'ERROR':
                    print(status)
                    break
                if status['status_code'] == 'FINISHED':
                    self.publish_content_ig(post_id, destroy_asset)
                    return ig_post_id

            except Exception as e:
                print(e)
                break
    
    
    def get_quota(self):

        extra = 'fields=config,quota_usage'

        cuota = requests.get(f'{self.instagram_url}content_publishing_limit?{extra}\
        &{self.ig_access_token_url}').json()

        return cuota['data'][0]
    


    def default_post_on_instagram(self, local_content,image_url):
        list_hashtags = HASHTAGS.objects.random_ig_hashtags

        hashtags = ' '.join([hashtag.name for hashtag in list_hashtags])
        
        title = DEFAULT_TITLES.objects.random_title
            

        ig_cap = self.create_ig_caption(title.title, hashtags)

        ig_id = self.post_ig(ig_cap, image_url = image_url)

        ig_post = INSTAGRAM_POST.objects.create(
            content_related = local_content,
            post_type = 2,
            title = title,
            social_id = ig_id,
        )

        for hashtag in list_hashtags:
            ig_post.hashtags.add(hashtag)

        return ig_id
    

    def get_media_info(self, media_id):
        url = f'{self.main_instagram_url}/{media_id}'
        params = {
            'fields':'media_url',
            'access_token':self.user_access_token
        }
        response = requests.get(url, params = params)
        print(response.content)
        return response.json()

        



    
    def create_ig_caption(self, title, hashtags):        
        instagram_caption = f"""
        {title}
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
        .
        .
        .
        .
        .
        {hashtags}
        """
        return instagram_caption
    


    def download_instagram():
    #create a list of users to download content from
    #create a function to check if there is a new image
    #edit the image if necessary
        pass