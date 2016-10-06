# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, redirect, url_for
import random
import config
from forms import EnterNumber

import logging

logger = logging.getLogger(__name__)

__author__ = 'kakoka'

def create_app():

    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)

    # задаем случайное число
    rnd_number = random.randint(1, 99)
    # и печатаем его в консоли, правда почему то оно два раза печатается... пока не понял
    print(rnd_number)

    @app.route('/', methods=['GET', 'POST'])
    def home():
        response = ''
        if request.method == 'POST':

            # запрашиваем данные формы

            form = EnterNumber(request.form)

            if form.validate():
                # если прошли валидацию - саму валидацию смотри в файле forms.py
                # сравниваем поле формы с числом с помощью if

                if form.data['number']:
                    if form.data['number'] < rnd_number:
                        response = "Меньше!"
                        pass
                    elif form.data['number'] > rnd_number:
                        response = "Больше!"
                        pass
                    else:
                        print(rnd_number)
                        response = "Угадал!"
                else:
                    form = EnterNumber()
            else:
                logger.error('Someone have submitted an incorrect form!')
        else:
            form = EnterNumber()
        return render_template(
            'home.html',
            form=form,
            items=response,
        )
    # надо придумать как рестартовать игру если угадал число
    # чего то туплю и не могу придумать

    return app

if __name__ == '__main__':

    create_app().run()