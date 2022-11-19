from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from json import load
from secrets import token_hex


with open('conf.json', 'r') as f:
    conf = load(f)

mysql_uri = f"mysql+pymysql://{conf['MYSQL']['USERNAME']}:{conf['MYSQL']['PASSWORD']}@{conf['MYSQL']['HOST']}:" \
            f"{conf['MYSQL']['PORT']}/{conf['MYSQL']['DB']}"

# create the extension
db = SQLAlchemy()

# create the app
app = Flask(__name__)  # initialize instance of Flask

# configure the MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = token_hex(12)

db.init_app(app)

login_manager = LoginManager(app)  # Login Manager
login_manager.login_view = 'login_page'  # redirect users to login page (see routes.py)
login_manager.login_message_category = 'info'

# careful of circular imports https://flask.palletsprojects.com/en/2.2.x/patterns/packages/
from flaskr import routes

with app.app_context():
    import flaskr.models
    db.create_all()


