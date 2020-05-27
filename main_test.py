from flask import Flask
from cogs import __all__

app = Flask(__name__)

if __name__ == '__main__':
    app.run(port=8080)
