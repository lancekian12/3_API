from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, make_response
import requests
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
import random


from .models import Users, Funds
from . import app, db


# Decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            print(token)

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
    first_name = data.get("first_name")
    last_name = data.get("last_name")

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


# Fetch Anime Details
@app.route("/anime", methods=["GET"])
@token_required
def get_anime(current_user):
    query = request.args.get("query")
    if not query:
        return {"message": "Anime query is required"}, 400

    try:
        response = requests.get(f"https://api.jikan.moe/v4/anime?q={query}")
        if response.status_code == 200:
            return response.json(), 200
        return {"message": "Failed to fetch anime details"}, response.status_code
    except Exception as e:
        print(f"Error fetching anime: {e}")
        return {"message": "An error occurred while fetching anime details"}, 500


# Fetch Movie Details
@app.route("/movie", methods=["GET"])
@token_required
def get_movie(current_user):
    query = request.args.get("query")
    if not query:
        return {"message": "Movie query is required"}, 400

    try:
        response = requests.get(f"https://ghibliapi.herokuapp.com/films")
        if response.status_code == 200:
            movies = response.json()
            filtered_movies = [
                movie for movie in movies if query.lower() in movie["title"].lower()
            ]
            return {"movies": filtered_movies}, 200
        return {"message": "Failed to fetch movie details"}, response.status_code
    except Exception as e:
        print(f"Error fetching movie: {e}")
        return {"message": "An error occurred while fetching movie details"}, 500


# Fetch Book Details
@app.route("/book", methods=["GET"])
@token_required
def get_book(current_user):
    query = request.args.get("query")
    if not query:
        return {"message": "Book query is required"}, 400

    try:
        response = requests.get(f"https://openlibrary.org/search.json?q={query}")
        if response.status_code == 200:
            return response.json(), 200
        return {"message": "Failed to fetch book details"}, response.status_code
    except Exception as e:
        print(f"Error fetching book: {e}")
        return {"message": "An error occurred while fetching book details"}, 500


@app.route("/recommendation", methods=["GET"])
def get_recommendation():
    anime_query = request.args.get("anime")
    book_query = request.args.get("book")
    dog_query = request.args.get("dog")

    results = {}

    # Handle Anime Recommendation
    if anime_query:
        anime_response = requests.get(f"https://api.jikan.moe/v4/anime?q={anime_query}")
        if anime_response.status_code == 200:
            anime_data = anime_response.json()
            results["anime"] = anime_data.get("data", [])
        else:
            results["anime"] = {"message": "Failed to fetch anime"}
    else:
        try:
            anime_response = requests.get(f"https://api.jikan.moe/v4/anime")
            if anime_response.status_code == 200:
                anime_data = anime_response.json()
                anime_list = anime_data.get("data", [])
                if anime_list:
                    random_anime = random.choice(anime_list)
                    results["anime"] = [random_anime]
                else:
                    results["anime"] = {"message": "No anime data available"}
            else:
                results["anime"] = {"message": "Failed to fetch random anime"}
        except Exception as e:
            results["anime"] = {"message": f"Error fetching random anime: {e}"}

    # Handle Book Recommendation
    if book_query:
        book_response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q={book_query}"
        )
        if book_response.status_code == 200:
            books = book_response.json().get("items", [])
            filtered_books = [
                {
                    "title": book["volumeInfo"].get("title"),
                    "author_name": book["volumeInfo"].get("authors", []),
                    "first_publish_year": book["volumeInfo"].get("publishedDate"),
                }
                for book in books
            ]
            results["book"] = (
                filtered_books
                if filtered_books
                else {"message": "No matching books found"}
            )
        else:
            results["book"] = {"message": "Failed to fetch book"}
    else:
        try:
            book_response = requests.get(
                "https://www.googleapis.com/books/v1/volumes?q=subject:fiction"
            )
            if book_response.status_code == 200:
                books = book_response.json().get("items", [])
                if books:
                    random_book = random.choice(books)
                    results["book"] = [
                        {
                            "title": random_book["volumeInfo"].get("title"),
                            "author_name": random_book["volumeInfo"].get("authors", []),
                            "first_publish_year": random_book["volumeInfo"].get(
                                "publishedDate"
                            ),
                        }
                    ]
                else:
                    results["book"] = {"message": "No books available"}
            else:
                results["book"] = {"message": "Failed to fetch random book"}
        except Exception as e:
            results["book"] = {"message": f"Error fetching random book: {e}"}

    # Handle Dog Breed Recommendation
    if dog_query:
        dog_response = requests.get(f"https://dog.ceo/api/breeds/image/random")
        if dog_response.status_code == 200:
            dog_data = dog_response.json()
            results["dog"] = {
                "breed_image": dog_data.get("message", ""),
                "message": "Random dog breed image",
            }
        else:
            results["dog"] = {"message": "Failed to fetch dog breed"}
    else:
        try:
            dog_response = requests.get(f"https://dog.ceo/api/breeds/image/random")
            if dog_response.status_code == 200:
                dog_data = dog_response.json()
                results["dog"] = {
                    "breed_image": dog_data.get("message", ""),
                    "message": "Random dog breed image",
                }
            else:
                results["dog"] = {"message": "Failed to fetch random dog breed"}
        except Exception as e:
            results["dog"] = {"message": f"Error fetching random dog breed: {e}"}

    # Return consolidated results
    return jsonify(results), 200
