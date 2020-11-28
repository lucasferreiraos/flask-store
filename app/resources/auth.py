import logging
import secrets
from base64 import b64decode

from app.extensions import db
from app.services.mail import send_mail
from app.models import User
from datetime import timedelta
from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash


class Login(Resource):

    def get(self):
        if not request.headers.get("Authorization"):
            return {"error": "authorizatiuon nao encontrado"}, 400

        basic, code = request.headers["Authorization"].split(" ")
        if not basic.lower() == "basic":
            return {"error": "autorizacao mal formatada"}, 400

        email, password = b64decode(code).decode().split(":")

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return {"error": "email e/ou senha invalidos"}, 400

        token = create_access_token(
            {"id": user.id}, expires_delta=timedelta(days=2)
        )

        return {"access_token": token}


class Register(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, help="O campo email é obrigatório")
        parser.add_argument(
            "password", required=True, help="O campo senha é obrigatório"
        )
        args = parser.parse_args()

        user = User.query.filter_by(email=args.email).first()
        if user:
            return {"error": "e-mail já registrado!"}, 400

        user = User()
        user.email = args.email
        user.password = generate_password_hash(args.password)

        db.session.add(user)
        try:
            db.session.commit()
            send_mail(
                "Bem vindo(a) a Flask Store", user.email, "welcome", email=user.email
            )

            return {"message": "Usuario registrado com sucesso"}, 201
        except Exception as e:
            db.session.rollback()
            logging.critical(str(e))
            return {"error": "nao foi possivel registrar o usuario"}, 500


class ForgetPassword(Resource):

    def post(self):
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument("email", required=True, help="o campo email e obrigatorio")
        args = parser.parse_args()

        user = User.query.filter_by(email=args.email).first()
        if not user:
            return {"error": "dados nao encontrados"}, 400

        password_temp = secrets.token_hex(8)
        user.password = generate_password_hash(password_temp)
        db.session.add(user)
        db.session.commit()

        send_mail(
            "Recuperação de senha",
            user.email,
            "forget-password",
            password_temp=password_temp,
        )
        return {"message": "email enviado com sucesso"}
