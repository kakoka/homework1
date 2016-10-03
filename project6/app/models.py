# -*- coding: utf-8 -*-

import datetime
from flask_login import UserMixin

__author__ = 'sobolevn'


class Storage(object):
    items = None
    _obj = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._obj is None:
            cls._obj = object.__new__(cls)
            cls.items = []
        return cls._obj


class BlogPostModel(object):
    def __init__(self, form_data):
        # self.uid = uid
        self.title = form_data['title']
        self.text = form_data['text']
        # self.another_text = form_data['text']
        self.time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        self.author = form_data['author']


class User(UserMixin):
    # proxy for a database of users
    user_database = {"JohnDoe": ("JohnDoe", "John"),
               "JaneDoe": ("JaneDoe", "Jane")}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)
