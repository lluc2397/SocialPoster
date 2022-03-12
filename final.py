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


logo = '/home/lucas/InvFin/images/LOGO/logo FB Inversiones y finanzas.png'
def desktop_notification(title, message='', duration=1, img_path=logo):
    s.Popen(["notify-send",f"{title}", f"{message}", "-t",f"{(duration * 1000)}", "-i", f"{img_path}"])


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-short', "--short",  action='store_true',
    help='Post short video')

    parser.add_argument('-long', "--long", action='store_true',
    help='Post long video')

    parser.add_argument('-img', "--image", nargs='?', const='logos', default=False,
    help='Post image')

    parser.add_argument('-test', "--test", action='store_true',
    help='Test')  

    args_dict = vars(parser.parse_args())

    if all(value is False for value in list(args_dict.values())): 
        Multipostage().tests()
        desktop_notification("Selecciona una opción", message="'-short, -long ,-img o -test'")           

    if args_dict['long'] is True:
        Multipostage().share_long()

    if args_dict['image'] is not False:
        folder_name = args_dict['image']
        Multipostage().share_image(folder_name)
    
    if args_dict['short'] is True:
        Multipostage().share_short()
    
    if args_dict['test'] is True:        
        desktop_notification('Nop')

if __name__ == '__main__':
    main()