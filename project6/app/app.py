# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from wtf_tinymce import wtf_tinymce

import config
from forms import BlogPostForm
from models import Storage, BlogPostModel

import logging

logger = logging.getLogger(__name__)

__author__ = 'kakoka'

def create_app():

    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)
    wtf_tinymce.init_app(app)
    Bootstrap(app)

    @app.route('/', methods=['GET', 'POST'])
    def home():
        storage = Storage()
        all_items = storage.items

        if request.method == 'POST':
            form = BlogPostForm(request.form)
            if form.validate():
                model = BlogPostModel(form.data)
                all_items.append(model)
                storage.save()
                return redirect(url_for('home'))
            else:
                logger.error('Someone have submitted an incorrect form!')
        else:
            form = BlogPostForm()

        return render_template(
            'home.html',
            form=form,
            items=all_items,
        )
    return app

if __name__ == '__main__':

    create_app().run()
