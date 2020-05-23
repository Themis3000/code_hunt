from flask import Flask, render_template, send_from_directory
import os
import utils.test_data_sets
import utils.num_utils

app = Flask(__name__)


@app.route('/')
def index_page():
    return render_template("index.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'noggin.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/leaderboard/<code_type>')
@app.route('/leaderboard')
def leaderboard_page(code_type: str = 'ALL'):
    return render_template("leaderboard.html",
                           tops=utils.test_data_sets.tops_data,
                           code_type=code_type,
                           enumerate=enumerate,
                           amount_found=5,
                           amount_created=10,
                           total_scan_amount=7,
                           users_on_board=len(utils.test_data_sets.tops_data),
                           ordinal=utils.num_utils.ordinal,
                           user_placement=7)
