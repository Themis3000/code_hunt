from flask import Flask, render_template
import utils.test_data_sets

app = Flask(__name__)


@app.route('/')
def index_page():
    return render_template("index.html")


@app.route('/leaderboard/<code_type>')
@app.route('/leaderboard')
def leaderboard_page(code_type='ALL'):
    return render_template("leaderboard.html",
                           tops=utils.test_data_sets.tops_data,
                           code_type=code_type,
                           enumerate=enumerate)
