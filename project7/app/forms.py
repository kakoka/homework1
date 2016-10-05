# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField
from wtf_tinymce.forms.fields import TinyMceField

__author__ = 'kakoka'

class TextToQrForm(FlaskForm):
    text_to_qr = StringField(label='text_to_qr', validators=[
        validators.Length(min=4, max=140),
    ])