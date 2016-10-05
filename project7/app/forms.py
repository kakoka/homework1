# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, validators, BooleanField

__author__ = 'kakoka'

class TextToQrForm(FlaskForm):
    text_to_qr = StringField(label='Some text to QR-code, [4-140 symbols must be]', validators=[
        validators.Length(min=4, max=140),
    ])
    send_file = BooleanField('If you want to recieve file, please check this box', default=False)