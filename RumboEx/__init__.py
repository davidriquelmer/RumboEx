from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from werkzeug.security import check_password_hash,generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_rbac import RBAC
#from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
#app.config['RBAC_USE_WHITE'] = True
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/rumboex'
db = SQLAlchemy(app)
#jwt = JWTManager(app)

from RumboEx.model.role import Role
from RumboEx.model.user import User

rbac = RBAC(app)
rbac.set_user_loader(lambda : current_user)
rbac.set_user_model(User)
rbac.set_role_model(Role)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_current_user():
    with app.request_context():
        return current_user


everyone = Role('everyone')
logged_role = Role('logged_role')
logged_role.add_parent(everyone)

anonymous = User(roles=[everyone])
normal_user = User(roles=[logged_role])

current_user = anonymous




class UserLoginForm(Form):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=200)])
    remenber = BooleanField('remenber me')

@app.route('/')
def hello_world():
    return 'Bienvenidos a RumboEx ToDo'


@app.route('/login', methods=['GET', 'POST'])
@rbac.allow(roles=['everyone'], methods=['GET','POST'])
def login():
    form = UserLoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            print(hashed_password)
            if check_password_hash(user.password, form.password.data):
                print("AQUI 2")
                app.logger.debug('Logged in user %s', user.username)
                login_user(user, remember=form.remenber.data)
                return redirect(url_for('calendar'))
        error = 'Invalid username or password.'
    elif request.method == "POST":
        flash_errors(form)

    return render_template('login.html', form=form, error=error)

#hashed_password = generate_password_hash(form.password.data, method='sha56')

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            print(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))