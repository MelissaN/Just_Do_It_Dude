from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)


# security against modifying cookies and CSRF attacks
app.config['SECRET_KEY'] = 'tehe'


login_user = LoginManager(app)
login_user.login_view = 'login'
login_user.login_message = 'Ayah! Please sign in first'

from JDID import routes
