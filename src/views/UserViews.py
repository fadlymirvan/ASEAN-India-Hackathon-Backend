from flask import request, json, Response, Blueprint, g, jsonify
from ..models.UserModels import UserModels, UserSchema
from ..auth.Authentication import Auth

user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()


@user_api.route('/signup', methods=['POST'])
def SignUp():
    # Get Data
    data = request.get_json()
    try:
        data = user_schema.load(data)

    except Exception as err:
        return Response(mimetype="application/json", response=json.dumps({
            "message": err
        }), status=400)

    # Check If Email Exists in th DB
    is_user = UserModels.get_user_by_email(data.get('email'))
    if is_user:
        return Response(mimetype="application/json", response=json.dumps({
            "message": 'Email already taken, please use another email address.'
        }), status=400)

    # Save to database
    user = UserModels(data)
    user.save()

    # Generate Token
    user_dump = user_schema.dump(user)
    token = Auth.generate_token(user_dump.get('id'))

    return Response(mimetype="application/json", response=json.dumps({
        "message": "Created Successfully",
        "token": token,
    }), status=201)


@user_api.route('/signin', methods=['POST'])
def SignIn():
    data = request.get_json()
    try:
        data = user_schema.load(data, partial=True)

    except Exception as err:
        return Response(mimetype="application/json", response=json.dumps({
            "message": err
        }), status=400)
    is_user = UserModels.get_user_by_email(data.get('email'))
    if not data.get('email') or not data.get('password'):
        return Response(mimetype="application/json", response=json.dumps({
            "message": "Email and Password Cannot Be Empty!"
        }), status=400)

    if not is_user:
        return Response(mimetype="application/json", response=json.dumps({
            "message": "Invalid Email Address"
        }), status=400)

    if not is_user.check_hash(data.get('password')):
        return Response(mimetype="application/json", response=json.dumps({
            "message": "Invalid Password"
        }), status=400)

    # Generate Token
    user_data = user_schema.dump(is_user)
    token = Auth.generate_token(user_data.get('id'))

    return Response(mimetype="application/json", response=json.dumps({
        "message": "Login Successfully",
        "token": token
    }), status=200)
