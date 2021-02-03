from flask import json, Response, g
import datetime, jwt, os


class Auth():
    @staticmethod
    def generate_token(user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.getenv('JWT_SECRET_KEY'),
                'HS256'
            ).decode("utf-8")

        except Exception:
            return Response(
                mimetype="application/json", response=json.dumps({
                    "message" : "Error in Generating Token.",
                    "status": 400
                }), status=400)

    @staticmethod
    def decode_token(token):
        decode_token = {"data": {}, "error": {}}

        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
            decode_token['data'] = {'user_id': payload['sub']}
            return decode_token

        except jwt.ExpiredSignatureError:
            decode_token['error'] = {"message": "Token Expired, Please Login Again."}
            return decode_token

        except jwt.InvalidTokenError:
            decode_token['error'] = {"message": "Invalid Token, Please Try Again."}
            return decode_token
