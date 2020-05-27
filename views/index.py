from flask import render_template
from flask_classful import FlaskView
from main import limiter


class IndexView(FlaskView):
    route_base = '/'

    @limiter.exempt
    def index(self):
        return render_template("index.html")
