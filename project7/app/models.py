# -*- coding: utf-8 -*-

__author__ = 'kakoka'

class TextToQrModel(object):
    def __init__(self, form_data):
        self.text_to_qr = form_data['text_to_qr']
        self.send_file = form_data['send_file']
