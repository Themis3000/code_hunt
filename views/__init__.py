from utils.loaders import get_views
from flask import Flask


def init_views(app: Flask):
    for view in get_views():
        view.register(app)
