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
                with open(cls.filename, 'rt', encoding='utf-8') as file:
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
            json.dump(cls.items, file, default=json_default, indent=2)

class TextToQrModel(object):
    def __init__(self, form_data):
        self.text_to_qr = form_data['text_to_qr']

