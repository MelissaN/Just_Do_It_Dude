from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)


# security against modifying cookies and CSRF attacks
app.config['SECRET_KEY'] = 'ed19db85f910d4624779eda84eb9bc9b15c4a682'


login_user = LoginManager(app)
login_user.login_view = 'login'
login_user.login_message = 'Ayah! Please sign in first'

from JDID import routes
