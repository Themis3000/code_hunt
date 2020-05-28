from flask import render_template
from flask_classful import FlaskView


class ProfileView(FlaskView):
    route_base = '/user'

    def get(self, username):
        return render_template("profile.html",
                               username=username)
