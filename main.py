from flask import Flask
from views import init_views
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

app = Flask(__name__)
# limiter = Limiter(
#     app,
#     key_func=get_remote_address,
#     default_limits=["1/1second"])

init_views(app)
