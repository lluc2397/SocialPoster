import os
import json
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_keys(name):
    path_keys = os.path.abspath(os.path.join(os.path.dirname(__file__),'../keys.json'))
    keys_json = open(path_keys)
    data = json.load(keys_json)
    return data[name]

# SECURITY WARNING: Modify this secret key if using in production!
SECRET_KEY = "6few3nci_q_o@l1dlbk81%wcxe!*6r29yu629&d97!hiqat9fa"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INSTALLED_APPS = [
    "modelos",
    "socialmedias",
    "translate",
    ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'socialmedia',
        'USER': 'lucas',
        'PASSWORD': get_keys('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {  
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': './problemas.log',
#             'formatter': 'verbose',
#         },
#         'console': {
#             'class': 'logging.StreamHandler',
#             'level': 'DEBUG',
#         },   
        
#         # 'mail_admins': {
#         #     'level': 'ERROR',
#         #     'class': 'django.utils.log.AdminEmailHandler',
#         #     'filters': ['special']
#         # }
#     },
#     'loggers': {
#         # 'django': {
#         #     'handlers': ['file', 'console'],
#         #     'level': 'DEBUG',
#         #     'propagate': True,
#         # },
#         'screenerlog':{
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
            
#         }
#     }
# }