import datetime
import os
from uuid import uuid4 as uuid

import jwt
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_httpauth import HTTPTokenAuth
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from twilio.rest import Client

from models import User, Group, Base

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
    except Exception as exception:
        return exception


def init_endpoints(engine: Engine):
    Session.configure(bind=engine)

    @auth.verify_token
    def verify_token(token):
        data = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms='HS256')
        session = Session()

        user = session.query(User).filter_by(id=data["sub"]).first()
        return user

    @app.post('/register')
    @cross_origin()
    def register():
        session = Session()

        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = session.query(User).filter_by(email=post_data.get('email')).first()
        if user:
            response_object = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return jsonify(response_object), 202

        try:
            group = session.query(Group).filter_by(id=post_data.get('group_id')).first()
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

        except Exception as exception:
            print(exception)
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
            user = session.query(User).filter_by(email=post_data.get('email')).first()
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

        except Exception as exception:
            print(exception)
            response_object = {
                'status': 'fail',
                'message': str(exception)
            }
            return jsonify(response_object), 500

    @app.get('/group')
    @cross_origin()
    def get_group():
        session = Session()
        groups = session.query(Group).all()
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

        except Exception as exception:
            response_object = {
                'status': 'fail',
                'message': str(exception)
            }
            return jsonify(response_object), 500
        
    @app.post('/sms')
    @auth.login_required
    def sms():
        session = Session()
        my_phone = session.query(User).filter_by(id=user_id).first().phone
        all_phones = [u.phone for u in session.query(User).all()]
        phone_number = None
        for phone in all_phones:
            if phone != my_phone:
                phone_number = phone
        account_sid = 'AC8db8d6f7af13addc2bee16c95f9e3a9a' 
        auth_token = 'ebf123106d43cba081e81f8f2fdf577d' 
        client = Client(account_sid, auth_token)
        post_data = request.get_json()

        message = client.messages.create(  
                            messaging_service_sid='MGe9ac5c560345a70da6df56a735f0bea0', 
                            body='Heres your daily reminder to connect with your friends! \
                            Join the Slice of Life chat through this link: ' + post_data.get('link'),
                            to=phone_number
                        )
        return jsonify({"message": "success"})
        

if __name__ == '__main__':
    app.run()


def load_app():
    load_dotenv()
    engine = create_engine(os.getenv("DATABASE_URL"), connect_args={'sslmode': 'verify-ca'})
    Base.metadata.create_all(engine)
    init_endpoints(engine)
    print("Connected to database.")

    return app


if __name__ == "__main__":
    app = load_app()
    app.run()

