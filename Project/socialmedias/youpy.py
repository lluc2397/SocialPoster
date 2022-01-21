import httplib2
import os
import random
import shutil
import datetime
import time
import logging

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

from translate.google_trans_new import google_translator

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.select import Select


from models import (
    VIDEOS_TO_PARSE, 
    EMOJIS,
    DEFAULT_TITLES
)

# {related_links}

youtube_description = f"""

Prueba las herramientas que todo inversor inteligente necesita: https://inversionesyfinanzas.xyz

Visita nuestras redes sociales:
Facebook: https://www.facebook.com/Inversiones.y.Finanzas.Para.Todos
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

youtube_tags = "COMO INVERTIR, INVERTIR CON POCO DINERO, INVERTIR EN BOLSA, INVERTIR EN BOLSA, BOLSA DE VALORES, VALUE INVESTING, INVERSIÓN EN VALOR, INVERTIR FACIL, PUNTOS CLAVE PARA INVERTIR, INVERSIONES PARA PRINCIPIANTES, INVERTIR DESDE CERO"

short_tag = '#shorts'

translator = google_translator()
                                  
vertical_video_string = 'vertical-final.mp4'

yb_long_videos_folder = '/home/lucas/smcontent/yb-long-video/'


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



  def initialize_upload(self, video_title, video_file, post_time='', video_tags='', description=youtube_description, privacyStatus="private"):
    youtube = self.get_authenticated_service()
    tags = video_tags

    tags = tags.split(",")

    if video_title=='':
      video_title = random.choice(DEFAULT_TITLES.all())
      video_title = video_title.title


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
  def upload_caption(self, video_id, file, language = 'es', name = 'Español'):
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
  


  def new_video_to_parse(self, video_url, is_english = True, downloaded = False):
    try:
      yb_video = YouTube(video_url)

      has_caption = False

      if yb_video.captions:
        has_caption = True
      
      old_title = yb_video.title
      new_title = ''

      if is_english is True:        
        new_title = translator.translate(old_title, lang_src='en', lang_tgt='es')

      new_video = VIDEOS_TO_PARSE.create(
      url = video_url,
      original_channel = yb_video.author,
      old_title = old_title,
      new_title = new_title,
      downloaded = downloaded,
      has_caption = has_caption
      )

      return new_video
    except Exception as e:
      logging.error(f'Error al parse el video {video_url} ---> {e}')



  def parse_youtube_channel(self, channel_to_parse):
    """
    channel_to_parse has to be the channel's url
    """
    channel = Channel(channel_to_parse)
    all_videos = channel.video_urls
    for video_url in (all_videos):
      self.new_video_to_parse(video_url)

    print('Channel parsed')
  


  def download_youtube_video(self, video_url, get_captions = False, is_new = False, is_english = True):
    
    try:
        new_id = video_url
        new_dir = yb_long_videos_folder+new_id
        os.mkdir(new_dir)

        yb_video = YouTube(video_url)

        if is_new is True:
          self.new_video_to_parse(video_url, is_english, True)           
            
        yb_video.streams.get_highest_resolution().download(new_dir)            

        if get_captions is True:
          self.get_caption(new_dir, video_url)

    except Exception as e:
      logging.error(f'Error en la descarga del video {video_url} ---> {e}')
        
  


  def get_caption(self, new_dir, video_url):
    # Opciones de navegación
    options = Options()
    options.add_argument("headless")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("prefs", {
            "download.default_directory": f"{new_dir}",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
    })
    options.binary_location = '/opt/brave.com/brave/brave'
    driver_path = '/home/lucas/Programs/chromedriver_linux64/chromedriver'

    try:
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
        logging.error(f'Error en la descarga de captions del video {video_url} ---> {e}')
        os.rmdir(new_dir)
  


  def download_existing_videos(self, num):
    video_query = VIDEOS_TO_PARSE.query(downloaded = False, has_caption = True)[:num]

    for video in video_query:
        try:
          self.download_youtube_video(video.url, get_captions = True)
        except Exception as e:
            print('error al descargar en multipples', e)
            continue
        print('Video downloaded')
    print('Downloads finished')
  

  # def schedule_shorts_on_youtube(self, year, month, day, hour,number_to_post, contents_folder = posted_dir):
  #   folders = [folder for folder in os.listdir(contents_folder)]

  #   for folder in folders[:number_to_post]:
  #       complete_url_folder = f'{contents_folder}{folder}'

  #       vertical_url = f'{complete_url_folder}/{vertical_video_string}'
  #       hour += random.randrange(6, 9)
  #       minute = random.randrange(0, 59)
  #       if hour >= 24:
  #           hour = 0
  #           day += 1
  #       if day >=31:
  #           day = 1
  #           month += 1
  #       if month >= 13:
  #           month = 1
  #           year += 1

  #       yb_title = random.choice(titres_pour_youtube) + short_tag
  #       date = datetime.datetime(year, month, day,hour,minute)
  #       yb_date = date.strftime("%Y-%m-%dT%H:%M:%S")
  #       try:
  #           yb_vid_id = self.initialize_upload(yb_title, vertical_url, yb_date, youtube_tags, youtube_description)
            
  #           shutil.move(complete_url_folder, yb_pos+folder)
  #           desktop_notification('Youtube', f"Video id {yb_vid_id} was successfully uploaded.")
  #           MANAGE_RECORDS().update_record_yb(folder,yb_vid_id ,date)

  #       except Exception as e:
  #           desktop_notification('Youtube', f"Error con el video {complete_url_folder}")
  #           print(e)
  #           break
  


  def publish_downloaded_video_youtube(self, year, month, day, hour, number_to_post,contents_folder = yb_long_videos_folder):
    
    folders = [folder for folder in os.listdir(contents_folder)]
    
    for folder in folders[:number_to_post]:
        complete_url_folder = contents_folder+folder
        contents = os.listdir(complete_url_folder)

        for content in contents:
            if content.endswith("Spanish.srt"):
                srt_file = content
            if content.endswith(".mp4"):
                video_file = content
        video = VIDEOS_TO_PARSE.where(url = folder)

        yb_title = video.old_title
        if video.new_title != "":
            yb_title = video.new_title
      
        hour += random.randrange(6, 9)
        minute = random.randrange(0, 59)
        if hour >= 24:
            hour = 0
            day += 1
        if day >=31:
            day = 1
            month += 1
        if month >= 13:
            month = 1
            year += 1
        
        date = datetime.datetime(year, month, day,hour,minute)
        yb_date = date.strftime("%Y-%m-%dT%H:%M:%S")

        try:
            full_video_url = f'{complete_url_folder}/{video_file}'
            full_srt_url = f'{complete_url_folder}/{srt_file}'

            yb_vid_id = self.initialize_upload(yb_title, full_video_url, yb_date, youtube_tags, youtube_description)   
            self.upload_caption(yb_vid_id, full_srt_url)

        except Exception as e:
            print(e)
