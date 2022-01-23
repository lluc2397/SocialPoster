import httplib2
import os
import random
import shutil
import datetime
import time
import logging
import sys

from apiclient.discovery import build_from_document
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

from pytube import YouTube, Channel



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.select import Select



from modelos.models import (
  YOUTUBE_VIDEO_DOWNLOADED,
  FOLDERS,
  LOCAL_CONTENT,
  YOUTUBE_POST,
  HASHTAGS,
  DEFAULT_TITLES,
  youtube_description,
  EMOJIS)

from translate.google_trans_new import google_translator

short_tag = '#shorts'

translator = google_translator()
                                  
vertical_video_string = 'vertical-final.mp4'


# date = datetime.datetime(year, month, day,hour,minute)
# yb_date = date.strftime("%Y-%m-%dT%H:%M:%S")

class YOUTUBE:
  def __init__(self) -> None:
    self.MAX_RETRIES = 10
    self.RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
    self.RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
    self.CLIENT_SECRETS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../client_secrets.json"))
    self.YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
    self.YOUTUBE_API_SERVICE_NAME = "youtube"
    self.YOUTUBE_API_VERSION = "v3"
    self.YOUTUBE_PARTNER_SCOPE = "https://www.googleapis.com/auth/youtubepartner"
    self.YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
    self.MISSING_CLIENT_SECRETS_MESSAGE = MISSING_CLIENT_SECRETS_MESSAGE = """
            WARNING: Please configure OAuth 2.0

            To make this sample run you will need to populate the client_secrets.json file
            found at:

              %s

            with information from the API Console
            https://console.developers.google.com/

            For more information about the client_secrets.json file format, please visit:
            https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
            """ % os.path.abspath(os.path.join(os.path.dirname(__file__), self.CLIENT_SECRETS_FILE))



  def get_authenticated_service(self):
    flow = flow_from_clientsecrets(self.CLIENT_SECRETS_FILE,
      scope=self.YOUTUBE_UPLOAD_SCOPE,
      message=self.MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../UploadVideos-oauth2.json")))
    credentials = storage.get()

    if credentials is None or credentials.invalid:
      credentials = run_flow(flow, storage)

    return build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
      http=credentials.authorize(httplib2.Http()))



  def initialize_upload(self, video_title:str, video_file:str,  video_tags:list, description=youtube_description, post_time='', privacyStatus="private"):
    youtube = self.get_authenticated_service()
    tags = video_tags

    if privacyStatus == 'public':
      status = {
        'privacyStatus':privacyStatus
      }

    else:
      status = {
        'privacyStatus': privacyStatus,
        'publishAt':  post_time
      }

    body=dict(
    snippet=dict(
        title= video_title,
        description=description,
        tags=tags,
        categoryId="22"
    ),
    status=status
    )

    insert_request = youtube.videos().insert(
    part=",".join(body.keys()),
    body=body,
    media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True)
    )

    vid_id = self.resumable_upload(insert_request)
    return vid_id



  def get_authenticated_service_for_captions(self):
    flow = flow_from_clientsecrets(self.CLIENT_SECRETS_FILE,
      scope=self.YOUTUBE_READ_WRITE_SSL_SCOPE,
      message=self.MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../UploadCaptions-oauth2.json")))     
    credentials = storage.get()

    if credentials is None or credentials.invalid:
      credentials = run_flow(flow, storage)

    return build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
      http=credentials.authorize(httplib2.Http()))



  #upload captions
  def upload_caption(self, video_id:str, file:str, language = 'es', name = 'Español'):
    youtube = self.get_authenticated_service_for_captions()

    print('Uploading caption...')
    insert_result = youtube.captions().insert(
      part="snippet",
      body=dict(
        snippet=dict(
          videoId=video_id,
          language=language,
          name=name,
          isDraft=False
        )
      ),
      media_body=file
    ).execute()

    id = insert_result["id"]
    name = insert_result["snippet"]["name"]
    language = insert_result["snippet"]["language"]
    status = insert_result["snippet"]["status"]
    print (f"Uploaded caption track {name}, {id}, {language}, {status}")



  def resumable_upload(self, insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
      try:
        print ("Uploading file...")
        
        status, response = insert_request.next_chunk()
        if response is not None:
          if 'id' in response:
            return str(response['id'])
            
          else:
            exit("The upload failed with an unexpected response: %s" % response)
      except HttpError as e:
        if e.resp.status in self.RETRIABLE_STATUS_CODES:
          error = ("A retriable HTTP error %d occurred:\n%s" % e.resp.status, e.content)
        else:
          raise
      except self.RETRIABLE_EXCEPTIONS as e:
        error = ("A retriable error occurred: %s" % e)

      if error is not None:
        print (error)
        retry += 1
        if retry > self.MAX_RETRIES:
          exit("No longer attempting to retry.")

        max_sleep = 2 ** retry
        sleep_seconds = random.random() * max_sleep
        print ("Sleeping %f seconds and then retrying..." % sleep_seconds)
        time.sleep(sleep_seconds)
  


  def new_video_to_parse(self,channel_to_parse, video_url, is_english = True, downloaded = False):
    try:
      yb_video = YouTube(video_url)

      has_caption = False

      if yb_video.captions:
        has_caption = True
      
      old_title = yb_video.title
      new_title = ''

      if is_english is True:        
        new_title = translator.translate(old_title, lang_src='en', lang_tgt='es')

      new_video = YOUTUBE_VIDEO_DOWNLOADED.objects.create(
      url = video_url,
      original_channel = channel_to_parse,
      old_title = old_title,
      new_title = new_title,
      downloaded = downloaded,
      has_caption = has_caption
      )

      return new_video
    except Exception as e:
      logging.error(f'Error al parse el video {video_url} ---> {e}')



  def parse_youtube_channel(self, channel_to_parse:str):
    """
    channel_to_parse has to be the channel's url
    """
    channel = Channel(channel_to_parse.url)
    all_videos = channel.video_urls
    for video_url in (all_videos):
      self.new_video_to_parse(channel_to_parse,video_url)

    print('Channel parsed')
  


  def download_youtube_video(self, video_url:str, get_captions = True, is_new = False, is_english = True):
    
    try:
        yb_long_folder = FOLDERS.objects.get_or_create(full_path = '/home/lucas/smcontent/yb-long-video/')[0]
        print('Getting folder', yb_long_folder)
        
        local_content = LOCAL_CONTENT.objects.create(main_folder = yb_long_folder)
        print('Creating local content', local_content)

        new_dir = f'{local_content.local_path}'
        print('Creating new directory', new_dir)

        os.mkdir(new_dir)

        yb_video = YouTube(video_url)

        if is_new is True:
          self.new_video_to_parse(video_url, is_english, True)           
        
        print('Downloading video')
        yb_video.streams.get_highest_resolution().download(new_dir)            

        if get_captions is True:
          self.get_caption(local_content, video_url)
        
        print('returning')
        return local_content

    except Exception as e:
      print(f'Error en la descarga del video {video_url} ---> {e}')
      local_content.delete()
      os.rmdir(f'{local_content.local_path}')
        
  


  def get_caption(self, local_content, video_url:str):
    # Opciones de navegación
    options = Options()
    options.add_argument("headless")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("prefs", {
            "download.default_directory": f"{local_content.local_path}",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
    })
    options.binary_location = '/opt/brave.com/brave/brave'
    driver_path = '/home/lucas/Programs/chromedriver_linux64/chromedriver'

    try:
        print('starting to get captions')
        url = f'https://savesubs.com/process?url={video_url}'
        driver = webdriver.Chrome( executable_path = driver_path, options=options)
        driver.get(url)

        time.sleep(5)

        select_element = driver.find_element_by_name('slang')
        select_object = Select(select_element)
        select_object.select_by_value('en')

        select_element = driver.find_element_by_name('tlang')
        select_object = Select(select_element)
        select_object.select_by_value('es')

        select_element = driver.find_element_by_name('ext')
        select_object = Select(select_element)
        select_object.select_by_value('srt')
        # select_object.select_by_value('txt')

        button = driver.find_element_by_xpath('/html/body/main/section/main/section[3]/section/div[2]/div/form/button')

        button.click()
        time.sleep(1)
        driver.close()
    except Exception as e:
        print(f'Error en la descarga de captions del video {video_url} ---> {e}')
        local_content.delete()
        os.rmdir(f'{local_content.local_path}')


  def upload_and_post_video_youtube(self,local_content_related,post_type:int, yb_title='',is_original=False, with_caption=True,privacyStatus='public'):
    """
    if post_type == 1 video is long, if post_type == 2 is short
    """
    try:
      youtube_record = YOUTUBE_POST.objects.create(
        content_related = local_content_related,
        post_type = post_type,
        is_original = is_original
      )

      emojis = EMOJIS.objects.all()

      emoji1 = random.choice(emojis)
      emoji2 = random.choice(emojis)

      if yb_title == '':
        titles = [al_title for al_title in DEFAULT_TITLES.objects.all()]
        random_yb_title = random.choice(titles)
        youtube_record.default_title = random_yb_title
        yb_title = random_yb_title.title
      else:
        youtube_record.title = yb_title

      yb_title = f'{emoji1.emoji} {yb_title}{emoji2.emoji}'

      video_dir = f'{local_content_related.local_path}'

      if post_type == 1:
        for file in os.listdir(video_dir):
          if file.endswith('.mp4'):
            video_path = video_dir +file
          if file.endswith('.srt'):
            captions_path = video_dir +file
          print(f'{captions_path}')
      else:
        video_path = f'{video_dir}vertical-final.mp4'
        yb_title = yb_title + short_tag

      youtube_record.emojis.add(emoji1)
      youtube_record.emojis.add(emoji2)

      yb_hashtags = []
      for hashtag in HASHTAGS.objects.filter(for_yb = True):
        youtube_record.hashtags.add(hashtag)
        yb_hashtags.append(hashtag.name)
      

      yb_post_id = self.initialize_upload(video_title=yb_title, video_file=video_path,  video_tags=yb_hashtags, description=youtube_description, privacyStatus=privacyStatus)
      
      if with_caption is True:
        self.upload_caption(yb_post_id,captions_path)

      youtube_record.social_id = yb_post_id
      youtube_record.save()
      local_content_related.published = True
      local_content_related.save()

      return yb_post_id

    except Exception as e:
      print(e)