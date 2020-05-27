from flask import send_from_directory
from os.path import abspath, dirname, join
from flask_classful import FlaskView


PROJ_DIR = abspath(join(dirname(abspath(__file__)), '../'))


class FaviconView(FlaskView):
    route_base = '/favicon.ico'

    def index(self):
        return send_from_directory(join(PROJ_DIR, 'static'),
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')
