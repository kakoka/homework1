# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from wtf_tinymce import wtf_tinymce

import config
from forms import TextToQrForm
from models import Storage, TextToQrModel
from flask_qrcode import QRcode
from flask import send_file
import logging

logger = logging.getLogger(__name__)

__author__ = 'kakoka'

def create_app():

    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)
    wtf_tinymce.init_app(app)
    Bootstrap(app)
    QRcode(app)

    #@app.route("/qrgenerator/image.jpg")
    def generateQRImage(image):
        #response = make_response(qrWrapper.generateRandomQR())

        temp_location = '/tmp/image.jpg'

        # Save the qr image in a temp location
        image_file = open(temp_location, 'wb')
        image_file.write(image)
        image_file.close

        # Construct response now
        response.headers["Content-Type"] = "image/jpeg"
        response.headers["Content-Disposition"] = "attachment; filename=image.jpg"
        return send_file(temp_location)

    @app.route('/', methods=['GET', 'POST'])
    def home():
        storage = Storage()
        all_items = storage.items

        if request.method == 'POST':
            form = TextToQrForm(request.form)
            if form.validate():
                img_link = make_response(TextToQrModel(form.data))
                model = TextToQrModel(form.data, img_link)
                all_items.append(model)
                storage.save()
                return redirect(url_for('home'))
            else:
                logger.error('Someone have submitted an incorrect form!')
        else:
            form = TextToQrForm()

        return render_template(
            'home.html',
            form=form,
            items=all_items,
        )
    return app

if __name__ == '__main__':

    create_app().run()
