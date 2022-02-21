import os
import sys
import json
from pathlib import Path
import cloudinary
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Motdepasse:
    def __init__(self) -> None:
        self.KEYS_PATH = os.path.join(Path(__file__).resolve().parent.parent,'keys.json')

    def get_keys(self,name):    
        with open(self.KEYS_PATH, 'r') as keys_json:
            data = json.load(keys_json)
        return data[name]

    def change_key_value(self,key, value):
        with open(self.KEYS_PATH, 'r') as keys_json:
            data = json.load(keys_json)
        
        data[key] = value

        with open(self.KEYS_PATH, 'w') as keys_json:
            json.dump(data, keys_json)


def error_handling(where, extra=None):
    def decorator(func):
        def wrap(*args, **kwargs):

            try:            
                result = func(*args, **kwargs)
                response ={
                    'result':'success',
                    'extra' : result
                    }
                
            except Exception as e:
                response ={
                    'result':'error',
                    'where':where,
                    'message':e,
                    'extra' : extra
                    }            
            
            return response
        return wrap
    return decorator


def print_progress_bar(current_position, total_size, extra_text):
    bar_size = 10 
    percentage = current_position/total_size
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(bar_size * percentage):{bar_size}s}] {int(100 * percentage)}%  {extra_text}")
    sys.stdout.flush()


cloudinary.config( 
  cloud_name = "inversionesfinanzas", 
  api_key = Motdepasse().get_keys('CLOUDINARY_API_KEY'), 
  api_secret = Motdepasse().get_keys('CLOUDINARY_SECRET'),
  secure = True
)

USE_TZ = True

# SECURITY WARNING: Modify this secret key if using in production!
SECRET_KEY = "6few3nci_q_o@l1dlbk81%wcxe!*6r29yu629&d97!hiqat9fa"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INSTALLED_APPS = [
    "modelos",
    ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'socialmedia',
        'USER': 'lucas',
        'PASSWORD': Motdepasse().get_keys('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        }
    },
    'handlers': {  
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/lucas/socialposter.log',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'longs':{
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
            
        }
    }
}