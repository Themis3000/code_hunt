from main_test import app
from flask import render_template
from flask_classful import FlaskView


class IndexView(FlaskView):

    def index(self):
        return render_template("index.html")


IndexView.register(app, '/')
