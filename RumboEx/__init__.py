from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
# app.config['RBAC_USE_WHITE'] = True
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/rumboex'

from RumboEx.model.user import db
#db.init_app(app)

from flask import render_template, send_from_directory
import os

from RumboEx.model.user import UserLoginForm
@app.route('/login')
def login():
    form = UserLoginForm()
    return render_template('login.html', form=form)

@app.route('/<path:filename>')
def file(filename):
    return send_from_directory(os.path.join(app.root_path, 'templates'), filename)

@app.route('/')
def index():
    return render_template('index.html')

from RumboEx.controller.UserController import users
app.register_blueprint(users, url_prefix='/api')