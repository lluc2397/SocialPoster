import tweepy
import random
import json
from settings import Motdepasse

from modelos.models import Hashtag, DefaultTilte, TwitterPostRecord

site = 'https://inversionesyfinanzas.xyz'



class Twitter:
    def __init__(self) -> None:
        self.CONSUMER_KEY = Motdepasse().get_keys('consumer_key')
        self.CONSUMER_SECRET = Motdepasse().get_keys('consumer_secret')
        self.ACCESS_TOKEN = Motdepasse().get_keys('access_token')
        self.ACCESS_TOKEN_SECRET = Motdepasse().get_keys('access_token_secret')
    

    def do_authenticate(self):
        auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)

        twitter_api = tweepy.API(auth)
        return twitter_api

    def tweet_text(self, status, lista_hashtags = Hashtag.objects.random_tw_hashtags):
        twitter_api = self.do_authenticate()
        
        hashtag1 = random.choice(lista_hashtags)
        hashtag2 = random.choice(lista_hashtags)
        hashtag3 = random.choice(lista_hashtags)

        tweet_content = f'{status} #{hashtag1.name} #{hashtag2.name} #{hashtag3.name}'

        response = twitter_api.update_status(tweet_content)

        return response._json

    
    def tweet_with_media(self, media_url, status=''):

        twitter_api = self.do_authenticate()
        print('Tweet uploading...')
        post_id = twitter_api.media_upload(media_url)
        print('Posting tweet...')
        response = twitter_api.update_status(status=status, media_ids=[post_id.media_id_string])
        print('Tweeted')
        return response._json
    

    def default_tweet_status(self):
        lista_hashtags = HASHTAGS.objects.random_tw_hashtags
        
        title = DEFAULT_TITLES.objects.random_title

        hashtag1 = random.choice(lista_hashtags)
        hashtag2 = random.choice(lista_hashtags)
        hashtag3 = random.choice(lista_hashtags)

        tw_status = f'{title} #{hashtag1} #{hashtag2} #{hashtag3}'

        twitter_post = TWITTER_POST.objects.create(
            is_local = False,
            default_title = title,
            caption = tw_status)
        
        twitter_post.hashtags.add(hashtag1)
        twitter_post.hashtags.add(hashtag2)
        twitter_post.hashtags.add(hashtag3)
        twitter_post.save()

        response = {
            'tw_status':tw_status,
            'twitter_post_model':twitter_post
        }

        return response
    

    def default_image_tweet(self,local_content, media_url):
        default_tweet = self.default_tweet_status()

        twitter_post = default_tweet['twitter_post_model']
        status = default_tweet['tw_status']

        post_id = self.tweet_with_media(media_url, status=status)

        twitter_post.content_related = local_content
        twitter_post.post_type = 6
        twitter_post.social_id = post_id['id']
        twitter_post.save()
    

    def default_short_tweet(self,local_content, media_url):
        default_tweet = self.default_tweet_status()

        twitter_post = default_tweet['twitter_post_model']
        status = default_tweet['tw_status']

        post_id = self.tweet_with_media(media_url, status=status)

        twitter_post.content_related = local_content
        twitter_post.post_type = 5
        twitter_post.social_id = post_id['id']
        twitter_post.save()
