import requests

from config.settings import Motdepasse

class Tiktok():
    def __init__(self, 
    client_key=Motdepasse().get_keys('TIKTOK_CLIENT_KEY'), 
    client_secret=Motdepasse().get_keys('TIKTOK_CLIENT_SECRET')):
        self.client_key = client_key
        self.client_secret = client_secret
        self.post_url = 'https://open-api.tiktok.com/share/video/upload/'


    def post_video(self, video_url= ""):

        files = {open(video_url, 'rb')}

        full_url = f'{self.post_url}?open_id={self.client_key}&access_token={self.client_secret}'

        re = requests.post(full_url)

        print(re.content)