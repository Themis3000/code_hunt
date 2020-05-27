from flask import Flask, render_template, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import utils.test_data_sets
import utils.num_utils

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per hour", "1 per second"])


@app.route('/')
@limiter.exempt
def index_page():
    return render_template("index.html")


@app.route('/favicon.ico')
@limiter.exempt
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/leaderboard')
@limiter.limit("2/5second")
def leaderboard_page():
    return render_template("leaderboard.html",
                           tops=utils.test_data_sets.tops_data,
                           enumerate=enumerate,
                           len=len,
                           amount_found=5,
                           amount_created=10,
                           total_scan_amount=7,
                           ordinal=utils.num_utils.ordinal,
                           user_placement=7)


@app.route('/code/<code_id>')
@limiter.limit("10/minute")
def code_page(code_id: str):
    return render_template("code.html",
                           code_data=utils.test_data_sets.code_data,
                           amount_created=106,
                           accessing_username="temi3",
                           enumerate=enumerate,
                           len=len,
                           list=list,
                           reversed=reversed)


@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template("error_templates/249.html",
                           error=e)
