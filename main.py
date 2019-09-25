from flask import Flask, render_template, request, redirect, url_for
from mongo import add_visit, get_code

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
            return render_template("/scan/" + style + ".html")
            # return redirect(url_for('index'))
    elif request.method == 'POST':
        code = request.headers.get('code')
        add = request.headers.get('add')
        if add == "true":
            code_data, type_data, type_all_data = add_visit(code)
        else:
            code_data, type_data, type_all_data = get_code(code)
        if code_data is None:
            return {"error": 400}, 400
        else:
            return {"code_data": code_data, "type_data": type_data, "type_all_data": type_all_data}, 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
