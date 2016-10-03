# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField
from wtf_tinymce.forms.fields import TinyMceField

__author__ = 'kakoka'

class BlogPostForm(FlaskForm):
    title = StringField(label='Title', validators=[
        validators.Length(min=4, max=140),
    ])
    text = TinyMceField(label='Article Text',
                        validators=[validators.length(min=10, max=5000)],
                        tinymce_options={'toolbar': 'undo | redo | bold italic | link | code',
                                                                'height': '200',
                                                                'width': '1000'}
    )
    author = StringField(label='Author',
                         validators=[
                            validators.Length(min=10, max=40),
                            validators.Regexp('^[a-zA-Zа-яА-Я][a-zA-Zа-яА-Я0-9-_\.]{1,25}', message='Pishi normalno!')
     ])