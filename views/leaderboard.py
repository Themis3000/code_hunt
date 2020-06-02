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
        if page not in range(1, pages+1):
            return redirect(url_for("LeaderboardView:index"))

        prev_pages = 1
        next_pages = 2
        # generates the page range based on the amount of desired previous pages and next pages for there to be around
        # the selected page in a best case, will always show prev_pages + next_pages + 1 if possible, otherwise will
        # scale down the amount displayed. Yes I know this is probably done poorly, but it works
        if page + next_pages >= pages:
            end_page = page + (pages - page)
            start_page = page - ((next_pages - (pages - page)) + prev_pages)
        else:
            end_page = page + next_pages if page != 1 else page + next_pages + 1
            start_page = page - prev_pages
        start_page = start_page if start_page >= 1 else 1
        page_range = range(start_page, end_page + 1)

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
                               display_page_range=page_range)
