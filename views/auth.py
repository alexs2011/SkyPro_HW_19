from flask import request
from flask_restx import Namespace, Resource, abort

from implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        username = req_json.get("username")
        password = req_json.get("password")
        if not (username and password):
            abort(400)

        tokens = auth_service.generate_tokens(username, password)
        if not tokens:
            abort(401)
        return tokens

    def put(self):
        req_json = request.json
        ref_token = req_json.get("refresh_token")
        if not ref_token:
            abort(400)

        tokens = auth_service.approve_refresh_token(ref_token)
        if not tokens:
            abort(401)
        return tokens
