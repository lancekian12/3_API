from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy.sql import func
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from .models import Users, Funds
from . import app, db


# Decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # JWT is passed in the request headers as Authorization
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            print(token)

        # Return 401 if token is not passed
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, "secret", algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data["id"]).first()
            if not current_user:
                return jsonify({"message": "User not found"}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except Exception as e:
            print(e)
            return jsonify({"message": "Token is invalid"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/login", methods=["POST"])
def login():
    auth = request.json

    if not auth or not auth.get("email") or not auth.get("password"):
        return make_response({"message": "Proper credentials not provided"}, 401)

    user = Users.query.filter_by(email=auth.get("email")).first()
    if not user:
        return make_response({"message": "Please create an account"}, 401)

    if check_password_hash(user.password, auth.get("password")):
        token = jwt.encode(
            {"id": user.id, "exp": datetime.utcnow() + timedelta(minutes=30)},
            "secret",
            "HS256",
        )
        return make_response(jsonify({"token": token}), 201)

    return make_response({"message": "Please check your credentials"}, 401)


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")  # Updated to match the model field
    last_name = data.get("last_name")  # Updated to match the model field

    if not first_name or not last_name or not email or not password:
        return make_response({"message": "All fields are required"}, 400)

    try:
        user = Users.query.filter_by(email=email).first()
        if user:
            return make_response(
                {"message": "User already exists. Please Sign In."}, 409
            )

        user = Users(
            email=email,
            password=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name,
        )

        db.session.add(user)
        db.session.commit()
        return make_response({"message": "User Created Successfully"}, 201)
    except Exception as e:
        print(f"Error during signup: {e}")
        return make_response(
            {"message": "Unable to create user. Please try again later."}, 500
        )


@app.route("/funds", methods=["GET"])
@token_required
def get_all_funds(current_user):
    funds = Funds.query.filter_by(userId=current_user.id).all()
    total_sum = 0
    if funds:
        total_sum = (
            Funds.query.with_entities(db.func.round(func.sum(Funds.amount), 2))
            .filter_by(userId=current_user.id)
            .scalar()
            or 0
        )

    return jsonify({"data": [row.serialize for row in funds], "sum": total_sum})


@app.route("/funds/<id>", methods=["PUT"])
@token_required
def update_fund(current_user, id):
    try:
        funds = Funds.query.filter_by(userId=current_user.id, id=id).first()
        if funds is None:
            return {"message": "Unable to update, fund not found"}, 404

        data = request.json
        amount = data.get("amount")
        if amount is not None:
            try:
                funds.amount = float(amount)
            except ValueError:
                return {"message": "Invalid amount provided"}, 400

        db.session.commit()
        return {"message": funds.serialize}, 200
    except Exception as e:
        print(e)
        return {"error": "Unable to process"}, 409


@app.route("/funds", methods=["POST"])
@token_required
def post_fund(current_user):
    data = request.json
    amount = data.get("amount")
    if amount is None:
        return {"message": "Amount is required"}, 400

    try:
        fund = Funds(amount=float(amount), userId=current_user.id)
        db.session.add(fund)
        db.session.commit()
        return fund.serialize, 201
    except ValueError:
        return {"message": "Invalid amount provided"}, 400
    except Exception as e:
        print(e)
        return {"message": "Unable to create fund"}, 500


@app.route("/funds/<id>", methods=["DELETE"])
@token_required
def delete_fund(current_user, id):
    try:
        funds = Funds.query.filter_by(userId=current_user.id, id=id).first()
        if funds is None:
            return {"message": f"Fund with id {id} not found"}, 404

        db.session.delete(funds)
        db.session.commit()
        return {"message": "Fund deleted successfully"}, 202
    except Exception as e:
        print(e)
        return {"error": "Unable to process"}, 409
