from flask import render_template
from flask_classful import FlaskView
from utils.test_data_sets import code_data


class CodeView(FlaskView):
    route_base = '/code'

    def get(self, code_id):
        return render_template("code.html",
                               code_data=code_data,
                               amount_created=106,
                               accessing_username="temi3",
                               enumerate=enumerate,
                               len=len,
                               list=list,
                               reversed=reversed)
