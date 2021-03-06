import httplib2
import os
import random
import shutil
import time
import logging

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

from pytube import YouTube, Channel

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.select import Select

from modelos.models import (
  DefaultTilte,
  YoutubePostRecord,
  YoutubeChannel,
  YoutubeVideoDowloaded,
  Emoji,
  LocalContent,
  Folder,
  Hashtag
)

from config.settings import error_handling

from translate.google_trans_new import google_translator


youtube_description = f"""

Prueba las herramientas que todo inversor inteligente necesita: https://inversionesyfinanzas.xyz

Visita nuestras redes sociales:
Facebook: https://www.facebook.com/InversionesyFinanzas/
Instagram: https://www.instagram.com/inversiones.finanzas/
TikTok: https://www.tiktok.com/@inversionesyfinanzas?
Twitter : https://twitter.com/InvFinz
LinkedIn : https://www.linkedin.com/company/inversiones-finanzas

En este canal de INVERSIONES & FINANZAS, aprende cómo realizar un BUEN ANÁLISIS de las EMPRESAS. Descubre dónde invertir y de qué forma ENCONTRAR BUENAS OPORTUNIDADES de INVERSIÓN.

APRENDE como invertir en la bolsa de valores.🥇 DESCUBRE las mejores ESTRATEGIAS que existen para INVERTIR y los pasos que deberías seguir para INVERTIR en la BOLSA mexicana de VALORES. ¿Quieres CONOCER la forma de INVERTIR de los INVERSORES más célebres de forma clara y FÁCIL? ADÉNTRATE en el ASOMBROSO mundo de las INVERSIONES. Si lo  que buscas es aprender a : 
invertir en la bolsa de valores
invertir sin dinero
invertir con poco dinero
invertir siendo joven
multiplicar tu dinero
analizar una empresa
"""

translator = google_translator()

logger = logging.getLogger('longs')
# date = datetime.datetime(year, month, day,hour,minute)
# yb_date = date.strftime("%Y-%m-%dT%H:%M:%S")

class Youtube:
  def __init__(self) -> None:
    self.MAX_RETRIES = 10
    self.RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
    self.RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
    self.CLIENT_SECRETS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../client_secrets.json"))
    self.YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
    self.YOUTUBE_FULL_ACCESS_SCOPE = 'https://www.googleapis.com/auth/youtube'
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


  def _youtube_authentication(self):
    flow = flow_from_clientsecrets(self.CLIENT_SECRETS_FILE,
      scope=[self.YOUTUBE_UPLOAD_SCOPE, self.YOUTUBE_READ_WRITE_SSL_SCOPE, self.YOUTUBE_FULL_ACCESS_SCOPE],
      # scope = self.YOUTUBE_FULL_ACCESS_SCOPE,
      message=self.MISSING_CLIENT_SECRETS_MESSAGE)
    
    storage = Storage(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../TotalPerms-oauth2.json")))
    credentials = storage.get()

    if credentials is None or credentials.invalid:
      credentials = run_flow(flow, storage)

    return build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
      http=credentials.authorize(httplib2.Http()))


  @error_handling('initialize upload youtube video')
  def initialize_upload(self, video_title:str, video_file:str,  video_tags:list, description=youtube_description, post_time='', privacyStatus="private"):
    youtube = self._youtube_authentication()

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
        tags=video_tags,
        categoryId="22"
    ),
    status=status
    )

    insert_request = youtube.videos().insert(
    part=",".join(body.keys()),
    body=body,
    media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True)
    )

    vid_id = self._resumable_upload(insert_request)
    return vid_id


  def _resumable_upload(self, insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
      try:
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


  @error_handling('upload caption youtube video')
  def upload_caption(self, video_id:str, captions_file:str, language = 'es', name = 'Español'):
    youtube = self._youtube_authentication()
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
      media_body=captions_file
    ).execute()

    return video_id

  @error_handling('list captions youtube video')
  def list_captions(self, video_id):
    youtube = self._youtube_authentication()
    results = youtube.captions().list(
      part="snippet",
      videoId=video_id
    ).execute()

    for item in results["items"]:
      id = item["id"]
      name = item["snippet"]["name"]
      language = item["snippet"]["language"]
      print (f"Caption track '{name}({id})' in '{language}' language.")

    return results["items"]


  def new_video_to_parse(self,channel_to_parse, video_url, is_english = True):

    yb_video = YouTube(video_url)

    has_caption = False

    if yb_video.captions:
      has_caption = True
    
    old_title = yb_video.title
    new_title = ''

    if is_english is True:        
      new_title = translator.translate(old_title, lang_src='en', lang_tgt='es')

    new_video = YoutubeVideoDowloaded.objects.create(
      url = video_url,
      original_channel = channel_to_parse,
      old_title = old_title,
      new_title = new_title,
      downloaded = False,
      has_caption = has_caption
      )
    return new_video


  def parse_youtube_channel(self, channel_to_parse, keep_scraping = True, download_videos = True):
    """
    channel_to_parse can be the YoutubeChannel model or a url (str)
    """
    if type(channel_to_parse) == str:
      channel = Channel(channel_to_parse)
      channel_to_parse = YoutubeChannel.objects.get_or_create(
        name = channel.channel_name,
        url = channel_to_parse,
        keep_scraping= keep_scraping,
      )[0]
    else:
      channel = Channel(channel_to_parse.url)

    all_videos = channel.video_urls
    if download_videos == True:
      for video_url in (all_videos):
        self.new_video_to_parse(channel_to_parse,video_url)
        channel_to_parse.all_parsed = True
        channel_to_parse.save()    

    return all_videos
  


  def download_youtube_video(self, video, get_captions = True, is_new = False, is_english = True):
    
    yb_long_folder = Folder.objects.longs_folder
    
    local_content = LocalContent.objects.create(main_folder = yb_long_folder)
    video.content_related = local_content
    video.save()
    new_dir = f'{local_content.local_path}'

    os.mkdir(new_dir)

    video_url = video.url
    yb_video = YouTube(video_url)

    if is_new is True:
      self.new_video_to_parse(video_url, is_english, True)           
    try:
      yb_video.streams.get_highest_resolution().download(new_dir)
      video.downloaded = True
      video.save()

    except Exception as e:        
      local_content.delete()
      os.rmdir(f'{new_dir}')
      logger.error(f'Error en la descarga del video {video} ---> {e}')

    else:
      if get_captions is True:
        try:
          self.get_caption(local_content, video)     
        except Exception as e:
          logger.error(f'Error en la descarga de captios del video {video} ---> {e}')
      
      
      return local_content


  def get_caption(self, local_content, video):
    options = Options()
    options.add_argument("headless")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions") # disabling extensions
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage") # overcome limited
    options.add_experimental_option("prefs", {
            "download.default_directory": f"{local_content.local_path}",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
    })
    
    response = {}

    try:
      driver = webdriver.Chrome( executable_path = '/usr/lib/chromium-browser/chromedriver', options=options)
      
    except Exception as e:
      response['result'] = 'error'
      response['where'] = 'selenium driver'
      response['message'] = e
      
    else:
      try:
        driver.get(f'https://savesubs.com/process?url={video.url}')

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
        driver.quit()
        driver.stop_client()
        video.captions_downloaded = True
        video.save()
        response['result'] = 'success'
      except Exception as e:
        response['result'] = 'error'
        response['where'] = 'selenium download'
        response['message'] = e

        local_content.has_consistent_error = True
        local_content.error_msg = e
        local_content.save()
        driver.quit()
        driver.stop_client()
    finally:
      return response

  
  def upload_default_english_long_video(self, local_content, video, is_original=False):

    emojis = Emoji.objects.random_emojis(3)
    yb_hashtags = [hashtag.name for hashtag in Hashtag.objects.random_yb_hashtags]
    
    video_dir = local_content.local_path

    if video.new_title:
      custom_title = video.new_title
    else:
      try:
        custom_title = translator.translate(video.old_title, lang_src='en', lang_tgt='es')
      except Exception as e:
        logger.error(f'Unable to translate the title {e}')
        custom_title = video.old_title

    custom_title = f'{emojis[0].emoji} {custom_title}{emojis[1].emoji} en ESPAÑOL {emojis[2].emoji}(sub)'

    captions_path = False
    video_path = False
    for file in os.listdir(video_dir):
      if file.endswith('.mp4'):
        video_path = video_dir +file
      if file.endswith('.srt'):
        captions_path = video_dir +file

    if captions_path == False or video_path == False:
      logger.error(f'Captions {captions_path} video_path{video_path}')
      if captions_path == False:
        captions_response = self.get_caption(local_content, video)
        if captions_response['result'] == 'error':
          try:
            shutil.rmtree(video_dir)
            local_content.delete()
          except Exception as e:
            logger.error(f'Unable to delete the folder {e}')
            local_content.has_consistent_error = True
            local_content.error_msg = 'Needs to be deleted, has no captions available'
            local_content.save()
          return captions_response   

      if video_path == False:
        response = {
          'result':'error',
          'where':'upload long video',
          'message': 'No video path'
        }
        try:
          shutil.rmtree(video_dir)
          local_content.delete()
        except Exception as e:
          logger.error(f'Unable to delete the folder {e}')
          local_content.has_consistent_error = True
          local_content.error_msg = 'Needs to be deleted, has no video path'
          local_content.save()
        return response
    
    upload_video_response = self.initialize_upload(
      video_title=custom_title, 
      video_file=video_path,  
      video_tags=yb_hashtags, 
      description=youtube_description, 
      privacyStatus='public')

    if upload_video_response['result'] == 'success':
      local_content.published = True
      local_content.save()

      YoutubePostRecord.general_manager.save_record(
        local_content = local_content, 
        post_type =1, 
        is_original = is_original, 
        social_id = upload_video_response['extra'], 
        emojis = emojis, 
        hashtags = Hashtag.objects.random_yb_hashtags, 
        has_default_title = False,
        custom_title=custom_title,
        caption =youtube_description)

      upload_captions_response = self.upload_caption(video_id = upload_video_response['extra'], captions_file =captions_path)

      if upload_captions_response['result'] == 'error':
        local_content.has_consistent_error = True
        local_content.error_msg = upload_captions_response['message']
        local_content.save()
        
        mer_ms = upload_captions_response['message']
        logger.error(f'Error with captions {mer_ms}')
      return upload_captions_response

    else:
      local_content.has_consistent_error = True
      local_content.error_msg = upload_video_response['message']
      local_content.save()

      mer_ms = upload_video_response['message']
      logger.error(f'Error with upload {mer_ms}')
      return upload_video_response


  def upload_default_short(self, local_content, is_original=False, custom_title=''):

    emojis = Emoji.objects.random_emojis(2)
    yb_hashtags = [hashtag.name for hashtag in Hashtag.objects.random_yb_hashtags]

    use_default_title = False
    if custom_title == '':
      use_default_title = True
      default_title = DefaultTilte.objects.random_title
      custom_title = default_title.title
    custom_title = f'{emojis[0].emoji} {custom_title}{emojis[1].emoji} #shorts'

    upload_video_response = self.initialize_upload(
      video_title=custom_title, 
      video_file=local_content.local_vertical_short_path,  
      video_tags=yb_hashtags, 
      description=youtube_description, 
      privacyStatus='public')

    if upload_video_response['result'] == 'error':
      local_content.has_consistent_error = True
      local_content.error_msg = upload_video_response['message']
      local_content.save()

    else:
      local_content.published = True
      local_content.save()

      YoutubePostRecord.general_manager.save_record(
        local_content = local_content, 
        post_type =2, 
        is_original = is_original, 
        social_id = upload_video_response['extra'], 
        emojis = emojis, 
        hashtags = Hashtag.objects.random_yb_hashtags, 
        has_default_title =use_default_title, 
        default_title =default_title, 
        custom_title = custom_title,
        caption =youtube_description)
    
    return upload_video_response
    