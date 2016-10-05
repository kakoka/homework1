# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, send_file
from flask_bootstrap import Bootstrap

import config
from forms import TextToQrForm

from flask_qrcode import QRcode
import qrcode
import logging

logger = logging.getLogger(__name__)

__author__ = 'kakoka'

temp_location = 'tmp/you_qrcode.png'

def form_input_to_qr_image_file(form_field):
    a = qrcode.make(form_field)
    a.save("tmp/you_qrcode.png")
    return a

def create_app():

    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)
    Bootstrap(app)
    QRcode(app)

    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            form = TextToQrForm(request.form)
            if form.validate():
                if form.data['send_file']:
                    model = form.data['text_to_qr']
                    form_input_to_qr_image_file(model)
                    return send_file('tmp/you_qrcode.png')

                else:
                    model = form.data['text_to_qr']
                    form_input_to_qr_image_file(model)
                    pass
            else:
                logger.error('Someone have submitted an incorrect form!')
        else:
            form = TextToQrForm()

        return render_template(
            'home.html',
            form=form,
            send=form.data['send_file'],
            items=form.data['text_to_qr'],
        )

    @app.route('/tmp/you_qrcode.png', methods=['GET'])
    def send():
        return send_file('tmp/you_qrcode.png')

    return app

if __name__ == '__main__':

    create_app().run()
