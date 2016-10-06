# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import validators, IntegerField

__author__ = 'kakoka'

class EnterNumber(FlaskForm):

    # валидация - выбираем метод валидации NumberRange - в документации сказано что он как раз и контролирует какие циферки мы вводим

    number = IntegerField(label='Введи целое положительное число от 0 до 99', validators=[
        validators.NumberRange(min=1, max=99),
    ])
