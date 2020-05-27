from flask import render_template
from flask_classful import FlaskView
from utils.num_utils import ordinal
import utils.test_data_sets


class LeaderboardView(FlaskView):
    route_base = '/leaderboard'

    def index(self):
        return render_template("leaderboard.html",
                               tops=utils.test_data_sets.tops_data,
                               enumerate=enumerate,
                               len=len,
                               amount_found=5,
                               amount_created=10,
                               total_scan_amount=7,
                               ordinal=ordinal,
                               user_placement=7)
