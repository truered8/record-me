from typing import Callable
from uuid import uuid4 as uuid

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask_httpauth import HTTPTokenAuth
from twilio import twiml
import jwt
from twilio.rest import Client
import datetime

from db import CockroachService
from models import *

Session = sessionmaker()
app = Flask(__name__)
cors = CORS(app)
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
            session = Session()

            user = database.get_user(session, data["sub"])
            return user

        @app.post('/register')
        @cross_origin()
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
                group = database.get_group(session, post_data.get('group_id'))
                if not group:
                    response_object = {
                        'status': 'fail',
                        'message': f'Group with id {post_data.get("group_id")} does not exist.'
                    }
                    return jsonify(response_object), 401

                user = User(
                    id=uuid(),
                    email=post_data.get('email'),
                    password=post_data.get('password'),
                    phone=post_data.get('phone'),
                    group_id=post_data.get('group_id')
                )
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
        @cross_origin()
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
                    'message': str(e)
                }
                return jsonify(response_object), 500

        @app.get('/group')
        @cross_origin()
        def get_group():
            session = Session()
            groups = database.get_groups(session)
            response_object = {
                'status': 'success',
                'groups': [
                    {'name': group.name, 'id': group.id} for group in groups
                ]
            }
            return jsonify(response_object), 200

        @app.post('/group')
        @cross_origin()
        @auth.login_required
        def post_group():
            session = Session()

            # get the post data
            post_data = request.get_json()
            try:
                new_group = Group(
                    id=uuid(),
                    name=post_data.get('name')
                )
                session.add(new_group)
                session.commit()

                response_object = {
                    'status': 'success',
                    'message': 'Successfully added new group.',
                    'group_id': str(new_group.id)
                }
                return jsonify(response_object), 201

            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': str(e)
                }
                return jsonify(response_object), 500
            
        @app.post('/sms', methods=['POST'])
        @auth.login_required
        def sms():
            session = Session()
            phonenumber = database.get_phone(auth.current_user.id)
            account_sid = 'AC8db8d6f7af13addc2bee16c95f9e3a9a' 
            auth_token = '[AuthToken]' 
            client = Client(account_sid, auth_token)
            post_data = request.get_json()
            

            message = client.messages.create(  
                              messaging_service_sid='MGe9ac5c560345a70da6df56a735f0bea0', 
                              body='Heres your daily reminder to connect with your friends! Join the SliceofLife chat through this link: ' + post_data.get('link'),      
                              to=phonenumber 
                          )
            
            return print(message.sid)

if __name__ == '__main__':
    app.run()

        

    return init_endpoints


def load_app():
    database = CockroachService()
    database.connect(get_endpoint_loader(database))

    load_dotenv()
    return app


if __name__ == "__main__":
    app = load_app()
    app.run()
