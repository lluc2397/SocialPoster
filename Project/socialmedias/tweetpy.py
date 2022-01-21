import tweepy
import random
import json
from management import get_keys



site = 'https://inversionesyfinanzas.xyz'

lista_hashtags = [
    'invertir', 'inversiones', 'valueinvesting', 'invertirenvalor', 'inversionesinteligente',
    'bolsa', 'invertirenbolsa', 'inversorinteligente'
    ]



class TWITEER:
    def __init__(self) -> None:
        self.CONSUMER_KEY = get_keys('consumer_key')
        self.CONSUMER_SECRET = get_keys('consumer_secret')
        self.ACCESS_TOKEN = get_keys('access_token')
        self.ACCESS_TOKEN_SECRET = get_keys('access_token_secret')
    

    def do_authenticate(self):
        auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)

        twitter_api = tweepy.API(auth)
        return twitter_api

    def tweet_text(self, status):
        twitter_api = self.do_authenticate()
        hashtag1 = random.choice(lista_hashtags)
        hashtag2 = random.choice(lista_hashtags)
        hashtag3 = random.choice(lista_hashtags)

        tweet_content = f'{status} #{hashtag1} #{hashtag2} #{hashtag3}'

        response = twitter_api.update_status(tweet_content)

        return response._json

    
    def tweet_with_media(self, media_url, status):
        
        twitter_api = self.do_authenticate()
        post_id = twitter_api.media_upload(media_url)

        response = twitter_api.update_status(status=status, media_ids=[post_id.media_id_string])

        return response._json
    

status = 'caracol'
filename = '/home/lucas/smcontent/por_publicar/0a236d4b-c8bd-4d8b-8185-f84ab645d913/horizontal-final.mp4'


t = TWITEER().tweet_text(status)

print(t)

print(t['id'])