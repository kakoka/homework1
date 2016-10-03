# -*- coding: utf-8 -*-
from datetime import timedelta

__author__ = 'sobolevn'


DEBUG = False
SECRET_KEY = 'This key must be secret!'
# WTF_CSRF_ENABLED = False
#BOOTSTRAP_USE_MINIFIED = True
#BOOTSTRAP_SERVE_LOCAL = False
REMEMBER_COOKIE_DURATION = timedelta(days=14)
try:
    from config_local import *
except ImportError:
    pass

