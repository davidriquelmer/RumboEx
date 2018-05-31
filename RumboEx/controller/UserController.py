from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, make_response
from RumboEx.model.role import Role
from RumboEx.model.user import User
from RumboEx.config.generic import SECRET_KEY
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, Api
import flask_restful
import jwt
from jwt import DecodeError, ExpiredSignature
from datetime import datetime, timedelta
from functools import wraps
from flask import g


users = Blueprint('users', __name__)
# http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
#schema = UsersSchema()


# JWT AUTh process start
def create_token(user):
    payload = {
        'sub': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')

# Login decorator function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            payload = parse_token(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function

# JWT AUTh process end

api = Api(users)


class Auth(Resource):

    def post(self):
        data = request.get_json(force=True)
        print(data)
        username = data['username']
        password = data['password']
        print(username)
        user = User.query.filter_by(username=username).first()
        print(user)
        hashed_password = generate_password_hash(password, method='sha256')
        print(hashed_password)
        if user == None:
            response = make_response(
                jsonify({"message": "Usuario no encontrado / User not found"}))
            response.status_code = 401
            return response
        if check_password_hash(user.password, password):
            token = create_token(user)
            response = make_response(jsonify({
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': token
            }))
            response.status_code = 201
            return response
        else:
            response = make_response(
                jsonify({"message": "invalid username/password yeeeeee entroooo"}))
            response.status_code = 401
            return response

api.add_resource(Auth, '/login')


# Adding the login decorator to the Resource class
class Resource(flask_restful.Resource):
    method_decorators = [login_required]


# Any API class now inheriting the Resource class will need Authentication
class UserR(Resource):

    def get(self):

        results = User.query.all()
        #users = schema.dump(results, many=True).data
        return jsonify({"users": users})


api.add_resource(UserR, '/jodete')

