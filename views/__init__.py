from utils.loaders import get_views
from flask import Flask, render_template


def init_views(app: Flask):
    for view in get_views():
        view.register(app)
    configure_errors(app)


def configure_errors(app: Flask):
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return render_template("error_templates/249.html",
                               error=e)
