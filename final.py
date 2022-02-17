#!/home/lucas/Programacion/socialmediaposter/venv/bin/python

import argparse
import os
import subprocess as s
import sys

sys.dont_write_bytecode = True

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

from management import Multipostage

"""
Crear post text --> Postear text en twitter y compartir el tweet en fb viejo
                --> Poster text en fb nuevo

Ver como publicar en Tiktok de forma automática.
Ver en Linkedin
Después probar con google business

Descargar imágenes de insta.
"""

logo = '/home/lucas/InvFin/images/LOGO/logo FB Inversiones y finanzas.png'
def desktop_notification(title, message='', duration=1, img_path=logo):
    s.Popen(["notify-send",f"{title}", f"{message}", "-t",f"{(duration * 1000)}", "-i", f"{img_path}"])

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-short', "--short",  action='store_true',
    help='Post a short video')

    parser.add_argument('-long', "--long", action='store_true',
    help='Post a long video')

    parser.add_argument('-img', "--image", action='store_true',
    help='Post a image')

    parser.add_argument('-test', "--test", action='store_true',
    help='Test')    

    args_dict = vars(parser.parse_args())

    if all(value is False for value in list(args_dict.values())):
        # Multipostage().download_captions()
        desktop_notification('Nop')           

    if args_dict['long'] is True:
        Multipostage().share_long()

    if args_dict['image'] is True:
        Multipostage().create_share_image()
    
    if args_dict['short'] is True:
        Multipostage().create_share_short()
    
    if args_dict['test'] is True:
        Multipostage().tests()
        desktop_notification('Nop')

if __name__ == '__main__':
    main()
   