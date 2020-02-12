from flask_classful import FlaskView


class Api(FlaskView):
    def index(self):
        return "test2"

