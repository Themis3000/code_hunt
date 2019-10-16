from flask import Flask, render_template, request, redirect, url_for
from mongo import add_visit, set_username, get_type_data, get_code_data_by_public_id, get_user_by_public_id, get_top, create_codes
from datetime import datetime
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/scan/<style>', methods=['GET', 'POST'])
@app.route('/scan', methods=['GET', 'POST'])
def scan_page(style='default'):
    if request.method == 'GET':
        code = request.args.get('code')
        if code:
            return render_template("/scan/" + style + ".html")
        else:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        new_username = request.headers.get('new_username')
        if new_username:
            set_username(new_username, request.headers.get('id'))
            return {"success": True}, 200
        else:
            code = request.headers.get('code')
            user_id = request.headers.get('user_id')
            code_data, user_data, type_data, new_user = add_visit(code, user_id)
            if code_data is None:
                return {"error": 400}, 400
            else:
                return {"code_data": code_data, "user_data": user_data, "type_data": type_data, "new_user": new_user}, 200


@app.route('/code/<code>', methods=['GET'])
def code_page(code):
    code_data = get_code_data_by_public_id(code)
    type_data = get_type_data(code_data["type"])
    return render_template("code.html",
                           type=code_data["type"],
                           code_num=code_data["created_number"],
                           type_num=type_data["created_amount"],
                           code_scans=code_data["uses"],
                           created_date=datetime.fromtimestamp(code_data["created_date"]).strftime('%Y/%m/%d %I:%M:%S %p'),
                           history=code_data["uses_data"],
                           length=len(code_data["uses_data"]),
                           timestamp=datetime.fromtimestamp,
                           strftime=datetime.strftime)


@app.route('/profile/<public_id>', methods=['GET'])
@app.route('/profile', methods=["GET"])
def profile_page(public_id=None):
    if public_id:
        user_data = get_user_by_public_id(public_id)
        if user_data:
            return render_template("profile.html",
                                   username=user_data["username"],
                                   visits=user_data["visits_counts"]["ALL"]["visits"],
                                   join_date=datetime.fromtimestamp(user_data["join_date"]).strftime('%Y/%m/%d %I:%M:%S %p'),
                                   code_data=user_data["codes"],
                                   visits_data=user_data["visits_counts"],
                                   timestamp=datetime.fromtimestamp,
                                   strftime=datetime.strftime)
        else:
            return render_template("profile_redirect.html")
    else:
        return render_template("profile_redirect.html")


@app.route('/leaderboards/<type>')
@app.route('/leaderboards')
def leaderboards_page(type='ALL'):
    return render_template("leaderboards.html",
                           tops=list(get_top(type, 15)),
                           type=type)


@app.route('/api/create', methods=['POST'])
def create_code():
    if request.headers.get('api_key') in os.environ['api_keys']:
        return {"codes": create_codes(request.headers.get('type'), int(request.headers.get('amount')))}, 200
    else:
        return {"error": "Forbidden"}, 403


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
