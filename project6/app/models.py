# -*- coding: utf-8 -*-

import datetime
import json
__author__ = 'kakoka'


class Storage(object):
    items = None
    _obj = None
    filename = 'database.json'

    # сохранение в json подсмотрено нагло у соседа

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._obj is None:
            cls._obj = object.__new__(cls)
            cls.items = []
            try:
                with open(cls.filename, 'rt') as file:
                    cls.items = json.load(file)
            except:
                pass
        return cls._obj

    @classmethod
    def save(cls):
        if cls.items is None:
            return
        def json_default(o):
            return o.__dict__
        with open(cls.filename, 'wt') as file:
            json.dump(cls.items, file, default=json_default, indent=4)

class BlogPostModel(object):
    def __init__(self, form_data):
        self.title = form_data['title']
        self.text = form_data['text']
        self.time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        self.author = form_data['author']
