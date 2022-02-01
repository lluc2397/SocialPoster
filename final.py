#!/home/lucas/Programacion/socialmediaposter/venv/bin/python

import logging
import argparse
import os
import sys

sys.dont_write_bytecode = True

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

logging.basicConfig(filename='./problemas.log', level=logging.WARNING)

from management import MULTIPOSTAGE,desktop_notification
from modelos.models import (
    LOCAL_CONTENT,
    YOUTUBE_VIDEO_DOWNLOADED,
    INSTAGRAM_POST)
"""

Descargar y publicar directamten los videos con subtítulos en Youtube. Compartir el link del video en Face y Twitter.

Descargar imágenes de insta.
Ver como publicar en Tiktok de forma automática.
Ver en Linkedin
Después probar con google business

"""


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-short', "--short",  action='store_true',
    help='Post a short video')

    parser.add_argument('-long', "--long", action='store_true',
    help='Post a long video')
    

    args_dict = vars(parser.parse_args())

    if all(value is False for value in list(args_dict.values())):
        desktop_notification('Nop')
        parser.error("It's necessary to select at least one social media")


    if args_dict['long'] is True:
        files = os.listdir('/home/lucas/InvFin/smcontent/yb-longs')
        video_posted = False
        for file in files:
            ls = LOCAL_CONTENT.objects.get(iden = file)
            if ls.published is False and ls.has_consistent_error is False:
                video = YOUTUBE_VIDEO_DOWNLOADED.objects.get(content_related = ls)

                dwnl_process= MULTIPOSTAGE().dwnl_post_share_new_long_yb_video(video)
                video_posted = True
                if dwnl_process == 'captions-error':
                    continue                    
                else:
                    break
        
        if video_posted is False:
            MULTIPOSTAGE().dwnl_post_share_new_long_yb_video()

    if args_dict['short'] is True:
        MULTIPOSTAGE().create_post_image()

if __name__ == '__main__':
    main()
    