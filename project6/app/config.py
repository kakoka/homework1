# -*- coding: utf-8 -*-

__author__ = 'kakoka'


DEBUG = False
SECRET_KEY = 'This key must be secret!'
#WTF_CSRF_ENABLED = False
#BOOTSTRAP_USE_MINIFIED = True
#BOOTSTRAP_SERVE_LOCAL = False
try:
    from config_local import *
except ImportError:
    pass

