from flask import render_template, redirect, url_for
from flask_classful import FlaskView
from utils.test_data_sets import code_data


class CodeView(FlaskView):
    route_base = '/code'

    def index(self):
        return redirect(url_for('IndexView:index'))

    def get(self, code_id):
        return render_template("code.html",
                               code_data=code_data,
                               amount_created=106,
                               accessing_username="temi3",
                               enumerate=enumerate,
                               len=len,
                               list=list,
                               reversed=reversed)
