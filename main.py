from flask import Flask, render_template, request, redirect, url_for
from utils.mongo import add_visit, set_username, get_type_data, get_code_data_by_public_id, get_user_by_public_id, get_top, create_codes, get_users
from datetime import datetime
import os
import json

app = Flask(__name__)
# todo:Themi Populate index.html with actual content
# todo:Themi Make username on past code historys update after changing username


@app.route('/')
def index_page():
    return render_template("index.html")


@app.route('/scan/<style>', methods=['GET', 'POST'])
@app.route('/scan', methods=['GET', 'POST'])
def scan_page(style='default'):
    if request.method == 'GET':
        code = request.args.get('code')
        if code:
            return render_template("/scan/" + style + ".html")
        else:
            return redirect(url_for('profile_page'))
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
    user_public_ids = []
    for code in code_data["uses_data"]:
        user_public_ids.append(code["public_id"])
    updated_users = get_users(user_public_ids, {"username": True, "public_id": True})
    updated_users_formatted = {}
    for user in updated_users:
        updated_users_formatted[user["public_id"]] = user["username"]
    type_data = get_type_data(code_data["type"])
    return render_template("code.html",
                           type=code_data["type"],
                           code_num=code_data["created_number"],
                           type_num=type_data["created_amount"],
                           code_scans=code_data["uses"],
                           created_date=code_data["created_date"],
                           history=code_data["uses_data"],
                           updated_users_formatted=updated_users_formatted,
                           length=len(code_data["uses_data"])
                           )


@app.route('/profile/<public_id>', methods=['GET'])
@app.route('/profile', methods=["GET"])
def profile_page(public_id=None):
    if public_id:
        user_data = get_user_by_public_id(public_id)
        if user_data:
            return render_template("profile.html",
                                   username=user_data["username"],
                                   visits=user_data["visits_counts"]["ALL"]["visits"],
                                   join_date=user_data["join_date"],
                                   code_data=user_data["codes"],
                                   visits_data=user_data["visits_counts"]
                                   )
        else:
            return render_template("profile_redirect.html")
    else:
        return render_template("profile_redirect.html")


@app.route('/leaderboards/<type>')
@app.route('/leaderboards')
def leaderboards_page(type='ALL'):
    tops = list(get_top(type, 15))
    type_data = get_type_data(type)
    if type in tops[0]["visits_counts"]:
        return render_template("leaderboards.html",
                               tops=tops,
                               type=type,
                               enumerate=enumerate,
                               amount_found=type_data["unique_visits"],
                               amount_created=type_data["created_amount"],
                               total_scan_amount=type_data["visits"])
    else:
        #error page here
        return "you a hecker dummy face", 404


@app.route('/api/create', methods=['POST'])
def create_code():
    if request.headers.get('api_key') in json.loads(os.environ['api_keys']):
        return {"codes": create_codes(request.headers.get('type'), int(request.headers.get('amount')))}, 200
    else:
        return {"error": "Forbidden"}, 403


@app.route('/changeid', methods=['GET'])
def change_id_page():
    return render_template("changeid.html")
