from flask import render_template, request, redirect, url_for
from flask_classful import FlaskView
from utils.num_utils import ordinal
import utils.test_data_sets

pages = 5


class LeaderboardView(FlaskView):
    route_base = '/leaderboard'

    def index(self):
        page = int(request.args.get('page', '1'))
        # redirects user if supplied page is not in the page range
        if not 1 <= page <= pages:
            return redirect(url_for("LeaderboardView:index"))

        # shifts the display_page_range so that it dosen't show the page 0 or pages+1
        modifier = -1
        if page == 1:
            modifier += 1
        elif page == pages:
            modifier += -1

        return render_template("leaderboard.html",
                               tops=utils.test_data_sets.tops_data,
                               enumerate=enumerate,
                               len=len,
                               amount_found=5,
                               amount_created=10,
                               total_scan_amount=7,
                               ordinal=ordinal,
                               user_placement=7,
                               page=page,
                               pages=pages,
                               display_page_range=range(page + modifier, page + 3 + modifier))
