#!/home/lucas/Documents/programacion/SocialPoster/venv/bin/python3.8

import logging
import argparse
import os
import sys

sys.dont_write_bytecode = True

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

from socialmedias.youpy import YOUTUBE

logging.basicConfig(filename='problemas.log', level=logging.WARNING)

from management import MULTIPOSTAGE

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
        parser.error("It's necessary to select at least one social media")


    if args_dict['long'] is True:
        pass

    if args_dict['short'] is True:
        pass

from modelos.models import YOUTUBE_CHANNELS

if __name__ == '__main__':
    # main()
    MULTIPOSTAGE().dwnl_post_share_new_long_yb_video()

