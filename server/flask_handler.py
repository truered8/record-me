from typing import Callable
from uuid import uuid4 as uuid

from flask import Flask, request, jsonify, make_response
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask_httpauth import HTTPTokenAuth
import jwt
import datetime

from db import CockroachService
from models import *

Session = sessionmaker()
app = Flask(__name__)
app.config.from_object('config.BaseConfig')
auth = HTTPTokenAuth(scheme='Bearer')


def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=60),
            'iat': datetime.datetime.utcnow(),
            'sub': str(user_id)
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def get_endpoint_loader(database: CockroachService) -> Callable[[Engine], None]:
    def init_endpoints(engine: Engine):
        Session.configure(bind=engine)

        @auth.verify_token
        def verify_token(token):
            data = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms='HS256')
            print(data)
            session = Session()
            user = database.get_user(session, data["sub"])
            return user

        @app.post('/register')
        def register():
            session = Session()

            # get the post data
            post_data = request.get_json()
            # check if user already exists
            user = database.get_user_by_email(session, post_data.get('email'))
            if user:
                response_object = {
                    'status': 'fail',
                    'message': 'User already exists. Please Log in.',
                }
                return jsonify(response_object), 202

            try:
                user = User(
                    id=uuid(),
                    email=post_data.get('email'),
                    password=post_data.get('password'),
                    phone=post_data.get('phone'),
                    group_id=post_data.get('group_id')
                )
                print(user)

                # insert the user
                session.add(user)
                session.commit()
                # generate the auth token
                auth_token = encode_auth_token(user.id)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                }
                return jsonify(response_object), 201
            except Exception as e:
                print(e)
                response_object = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return jsonify(response_object), 401


        @app.post('/login')
        def login():
            session = Session()

            # get the post data
            post_data = request.get_json()
            try:
                # fetch the user data
                user = database.get_user_by_email(session, post_data.get('email'))
                if not user:
                    response_object = {
                        'status': 'fail',
                        'message': 'User does not exist.'
                    }
                    return jsonify(response_object), 404

                if user.password != post_data.get('password'):
                    response_object = {
                        'status': 'fail',
                        'message': 'Wrong password.'
                    }
                    return jsonify(response_object), 401

                auth_token = encode_auth_token(user.id)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token
                }
                return jsonify(response_object), 200

            except Exception as e:
                print(e)
                response_object = {
                    'status': 'fail',
                    'message': 'Try again'
                }
                return jsonify(response_object), 500

    return init_endpoints


def load_app():
    database = CockroachService()
    database.connect(get_endpoint_loader(database))

    load_dotenv()
    return app


if __name__ == "__main__":
    app = load_app()
    app.run()
