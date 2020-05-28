from flask import render_template
from flask_classful import FlaskView


class IndexView(FlaskView):
    route_base = '/'

    def index(self):
        return render_template("index.html")
