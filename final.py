#!/home/lucas/Programacion/socialmediaposter/venv/bin/python

import logging
import argparse
import os
import subprocess as s
import sys

sys.dont_write_bytecode = True

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

from management import MULTIPOSTAGE
from modelos.models import (
    LOCAL_CONTENT,FOLDERS,
    YOUTUBE_VIDEO_DOWNLOADED)

logger = logging.getLogger('longs')


"""

Descargar imágenes de insta.
Ver como publicar en Tiktok de forma automática.
Ver en Linkedin
Después probar con google business

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

    parser.add_argument('-test', "--test", action='store_true',
    help='Test')

    parser.add_argument('-img', "--image", action='store_true',
    help='Post a image')
    

    args_dict = vars(parser.parse_args())

    if all(value is False for value in list(args_dict.values())):
        desktop_notification('Nop')
        parser.error("It's necessary to select at least one social media")


    if args_dict['long'] is True:
        files = os.listdir('/home/lucas/InvFin/smcontent/yb-longs')
        # video_posted = False
        for file in files:
            
            ls = LOCAL_CONTENT.objects.get(iden = file)
            if ls.published is False and ls.has_consistent_error is False:
                video = YOUTUBE_VIDEO_DOWNLOADED.objects.get(content_related = ls)
                
                result = MULTIPOSTAGE().share_new_long_yb_video(video)
                
                if result != 'success':
                    ls.has_consistent_error = True
                    ls.save()
                    continue
                else:
                    sys.exit()
            else:
                continue         
        
        # if video_posted is False:
        #     try:
        #         MULTIPOSTAGE().dwnl_post_share_new_long_yb_video()
        #     except:
        #         logger.error('Error desde final.py')                
        #     else:
        #         sys.exit()
            

    if args_dict['img'] is True:
        MULTIPOSTAGE().create_post_image()
    
    if args_dict['short'] is True:
        MULTIPOSTAGE().create_post_short()
    
    if args_dict['test'] is True:
        desktop_notification('Nop')
        
if __name__ == '__main__':
    # main()
    folds = FOLDERS.objects.all()
    for f in folds:
        print(f.name, f)
    # contents = LOCAL_CONTENT.objects.available_video
    # print(contents)