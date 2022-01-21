

import logging
import argparse

import sys
sys.dont_write_bytecode = True

# Django specific settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django
django.setup()

logging.basicConfig(filename='problemas.log', level=logging.WARNING)


"""
Publicar los shorts directamente en FB, Youtube y Twitter, transformarlo en foto y publicarlo en Insta.

Descargar y publicar directamten los videos con subtítulos en Youtube. Compartir el link del video en Face y Twitter.

Descargar imágenes de insta.
Ver como publicar en Tiktok de forma automática.
Ver en Linkedin
Después probar con google business

"""


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-shrt', "--short",  type=int, default=False,
    help='Post a short video')

    parser.add_argument('-long', "--long",  type=int, default=False,
    help='Post a long video')
    

    args_dict = vars(parser.parse_args())


    if all(value is False for value in list(args_dict.values())):
        parser.error("It's necessary to select at least one social media")


    if args_dict['long'] is True:
        pass

    if args_dict['short'] is True:
        pass





if __name__ == '__main__':
    main()
    
      
   