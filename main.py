from flask import Flask, render_template, request, redirect, url_for
from mongo import add_visit, set_username

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/scan/<style>', methods=['GET', 'POST'])
@app.route('/scan', methods=['GET', 'POST'])
def scan(style='default'):
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
            code_data, user_data, new_user = add_visit(code, user_id)
            if code_data is None:
                return {"error": 400}, 400
            else:
                return {"code_data": code_data, "user_data": user_data, "new_user": new_user}, 200


@app.route('/create', methods=['POST'])
def create():
    pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
