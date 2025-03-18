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


# -------------------------------------------------------------------
# JWT Decorator
# -------------------------------------------------------------------
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


# -------------------------------------------------------------------
# Basic Routes
# -------------------------------------------------------------------
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


# -------------------------------------------------------------------
# Funds Routes
# -------------------------------------------------------------------
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


# -------------------------------------------------------------------
# Weather Routes using WeatherAPI
# -------------------------------------------------------------------
WEATHER_API_KEY = "d76d4eb38e6d48f1924132518251803"
WEATHER_BASE_URL = "https://api.weatherapi.com/v1"


# Current Weather
@app.route("/weather", methods=["GET"])
@token_required
def get_weather(current_user):
    location = request.args.get("location")
    if not location:
        return jsonify({"message": "Location parameter is required"}), 400

    url = f"{WEATHER_BASE_URL}/current.json"
    params = {"key": WEATHER_API_KEY, "q": location}

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return (
            jsonify(
                {
                    "message": "Failed to fetch weather information",
                    "error": response.json(),
                }
            ),
            response.status_code,
        )

    return jsonify(response.json()), 200


# Weather Forecast
@app.route("/weather/forecast", methods=["GET"])
@token_required
def get_weather_forecast(current_user):
    location = request.args.get("location")
    days = request.args.get("days", 3)  # default to 3-day forecast
    if not location:
        return jsonify({"message": "Location parameter is required"}), 400

    url = f"{WEATHER_BASE_URL}/forecast.json"
    params = {"key": WEATHER_API_KEY, "q": location, "days": days}

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return (
            jsonify(
                {
                    "message": "Failed to fetch weather forecast",
                    "error": response.json(),
                }
            ),
            response.status_code,
        )

    return jsonify(response.json()), 200


# Weather History
@app.route("/weather/history", methods=["GET"])
@token_required
def get_weather_history(current_user):
    """
    Example usage:
      GET /weather/history?location=London&date=2023-03-15
    """
    location = request.args.get("location")
    date = request.args.get("date")  # format YYYY-MM-DD
    if not location or not date:
        return jsonify({"message": "location and date are required"}), 400

    url = f"{WEATHER_BASE_URL}/history.json"
    params = {"key": WEATHER_API_KEY, "q": location, "dt": date}

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return (
            jsonify(
                {"message": "Failed to fetch weather history", "error": response.json()}
            ),
            response.status_code,
        )

    return jsonify(response.json()), 200


# Weather Astronomy
@app.route("/weather/astronomy", methods=["GET"])
@token_required
def get_weather_astronomy(current_user):
    """
    Example usage:
      GET /weather/astronomy?location=New York&date=2023-08-20
    """
    location = request.args.get("location")
    date = request.args.get("date")  # format YYYY-MM-DD
    if not location or not date:
        return jsonify({"message": "location and date are required"}), 400

    url = f"{WEATHER_BASE_URL}/astronomy.json"
    params = {"key": WEATHER_API_KEY, "q": location, "dt": date}

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return (
            jsonify(
                {"message": "Failed to fetch astronomy data", "error": response.json()}
            ),
            response.status_code,
        )

    return jsonify(response.json()), 200


# Weather Timezone
@app.route("/weather/timezone", methods=["GET"])
@token_required
def get_weather_timezone(current_user):
    """
    Example usage:
      GET /weather/timezone?location=New York
    """
    location = request.args.get("location")
    if not location:
        return jsonify({"message": "location is required"}), 400

    url = f"{WEATHER_BASE_URL}/timezone.json"
    params = {"key": WEATHER_API_KEY, "q": location}

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return (
            jsonify(
                {"message": "Failed to fetch time zone data", "error": response.json()}
            ),
            response.status_code,
        )

    return jsonify(response.json()), 200


# -------------------------------------------------------------------
# Workout / Wger API Routes
# -------------------------------------------------------------------
def get_wger_access_token():
    token_url = "https://wger.de/api/v2/token"
    payload = {"username": "lancekian12@gmail.com", "password": "@52425978Qwqw"}
    token_response = requests.post(token_url, data=payload)
    if token_response.status_code != 200:
        return None, token_response.json()
    tokens = token_response.json()
    return tokens.get("access"), tokens.get("refresh")


# 1. List all workouts
@app.route("/workouts", methods=["GET"])
@token_required
def list_workouts(current_user):
    access_token, _ = get_wger_access_token()
    if not access_token:
        return jsonify({"message": "Failed to obtain wger access token"}), 500

    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://wger.de/api/v2/workout/"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return (
            jsonify({"message": "Failed to fetch workouts", "error": response.json()}),
            response.status_code,
        )

    return jsonify(response.json()), 200


# 2. Retrieve a specific workout by ID
@app.route("/workouts/<int:workout_id>", methods=["GET"])
@token_required
def get_workout_by_id(current_user, workout_id):
    access_token, _ = get_wger_access_token()
    if not access_token:
        return jsonify({"message": "Failed to obtain wger access token"}), 500

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://wger.de/api/v2/workout/{workout_id}/"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return (
            jsonify({"message": "Failed to fetch workout", "error": response.json()}),
            response.status_code,
        )

    return jsonify(response.json()), 200


# 3. Create a new workout
@app.route("/workouts", methods=["POST"])
@token_required
def create_workout(current_user):
    workout_data = request.json  # e.g. {"comment": "My new workout"}
    access_token, _ = get_wger_access_token()
    if not access_token:
        return jsonify({"message": "Failed to obtain wger access token"}), 500

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    url = "https://wger.de/api/v2/workout/"
    response = requests.post(url, json=workout_data, headers=headers)
    if response.status_code not in [200, 201]:
        return (
            jsonify({"message": "Failed to create workout", "error": response.json()}),
            response.status_code,
        )

    return jsonify(response.json()), 201


# 4. Update an existing workout
@app.route("/workouts/<int:workout_id>", methods=["PUT"])
@token_required
def update_workout(current_user, workout_id):
    workout_data = request.json
    access_token, _ = get_wger_access_token()
    if not access_token:
        return jsonify({"message": "Failed to obtain wger access token"}), 500

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    url = f"https://wger.de/api/v2/workout/{workout_id}/"
    response = requests.put(url, json=workout_data, headers=headers)
    if response.status_code not in [200, 202]:
        return (
            jsonify({"message": "Failed to update workout", "error": response.json()}),
            response.status_code,
        )

    return jsonify(response.json()), 200


# 5. Delete a workout
@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
@token_required
def delete_workout(current_user, workout_id):
    access_token, _ = get_wger_access_token()
    if not access_token:
        return jsonify({"message": "Failed to obtain wger access token"}), 500

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://wger.de/api/v2/workout/{workout_id}/"
    response = requests.delete(url, headers=headers)
    if response.status_code not in [200, 204, 202]:
        return (
            jsonify({"message": "Failed to delete workout", "error": response.json()}),
            response.status_code,
        )

    return jsonify({"message": "Workout deleted successfully"}), 200


# -------------------------------------------------------------------
# Additional Wger Endpoints (Days & Exercises)
# -------------------------------------------------------------------
@app.route("/days", methods=["GET"])
@token_required
def list_days(current_user):
    """
    Lists all day objects. Typically, each 'day' belongs to a workout.
    """
    access_token, _ = get_wger_access_token()
    if not access_token:
        return jsonify({"message": "Failed to obtain wger access token"}), 500

    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://wger.de/api/v2/day/"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return (
            jsonify({"message": "Failed to fetch days", "error": response.json()}),
            response.status_code,
        )

    return jsonify(response.json()), 200


@app.route("/days", methods=["POST"])
@token_required
def create_day(current_user):
    """
    Create a new day.
    Example JSON:
    {
      "training": 123,   # the workout ID
      "description": "Monday routine"
    }
    """
    day_data = request.json
    access_token, _ = get_wger_access_token()
    if not access_token:
        return jsonify({"message": "Failed to obtain wger access token"}), 500

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    url = "https://wger.de/api/v2/day/"
    response = requests.post(url, json=day_data, headers=headers)
    if response.status_code not in [200, 201]:
        return (
            jsonify({"message": "Failed to create day", "error": response.json()}),
            response.status_code,
        )

    return jsonify(response.json()), 201


@app.route("/days/<int:day_id>", methods=["GET"])
@token_required
def get_day_by_id(current_user, day_id):
    access_token, _ = get_wger_access_token()
    if not access_token:
        return jsonify({"message": "Failed to obtain wger access token"}), 500

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://wger.de/api/v2/day/{day_id}/"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return (
            jsonify({"message": "Failed to fetch day", "error": response.json()}),
            response.status_code,
        )

    return jsonify(response.json()), 200


@app.route("/days/<int:day_id>", methods=["PUT"])
@token_required
def update_day(current_user, day_id):
    """
    Example JSON:
    {
      "description": "Updated day description"
    }
    """
    day_data = request.json
    access_token, _ = get_wger_access_token()
    if not access_token:
        return jsonify({"message": "Failed to obtain wger access token"}), 500

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    url = f"https://wger.de/api/v2/day/{day_id}/"
    response = requests.put(url, json=day_data, headers=headers)
    if response.status_code not in [200, 202]:
        return (
            jsonify({"message": "Failed to update day", "error": response.json()}),
            response.status_code,
        )

    return jsonify(response.json()), 200


@app.route("/days/<int:day_id>", methods=["DELETE"])
@token_required
def delete_day(current_user, day_id):
    access_token, _ = get_wger_access_token()
    if not access_token:
        return jsonify({"message": "Failed to obtain wger access token"}), 500

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://wger.de/api/v2/day/{day_id}/"
    response = requests.delete(url, headers=headers)
    if response.status_code not in [200, 204, 202]:
        return (
            jsonify({"message": "Failed to delete day", "error": response.json()}),
            response.status_code,
        )

    return jsonify({"message": "Day deleted successfully"}), 200


@app.route("/exercises", methods=["GET"])
@token_required
def list_exercises(current_user):
    """
    Lists exercises. You can filter with query params, e.g. ?language=2 or ?limit=50
    """
    access_token, _ = get_wger_access_token()
    if not access_token:
        return jsonify({"message": "Failed to obtain wger access token"}), 500

    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://wger.de/api/v2/exercise/"
    # Pass along any query params from the client to wger
    response = requests.get(url, headers=headers, params=request.args)
    if response.status_code != 200:
        return (
            jsonify({"message": "Failed to fetch exercises", "error": response.json()}),
            response.status_code,
        )

    return jsonify(response.json()), 200


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
@token_required
def get_exercise_by_id(current_user, exercise_id):
    access_token, _ = get_wger_access_token()
    if not access_token:
        return jsonify({"message": "Failed to obtain wger access token"}), 500

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://wger.de/api/v2/exercise/{exercise_id}/"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return (
            jsonify({"message": "Failed to fetch exercise", "error": response.json()}),
            response.status_code,
        )

    return jsonify(response.json()), 200


@app.route("/exercises", methods=["POST"])
@token_required
def create_exercise(current_user):
    """
    Note: Typically, only admin/staff can create new exercises in wger.
    Example JSON:
    {
      "name": "My Custom Exercise",
      "description": "Testing custom exercise creation",
      "category": 10,
      "language": 2
    }
    """
    exercise_data = request.json
    access_token, _ = get_wger_access_token()
    if not access_token:
        return jsonify({"message": "Failed to obtain wger access token"}), 500

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    url = "https://wger.de/api/v2/exercise/"
    response = requests.post(url, json=exercise_data, headers=headers)
    if response.status_code not in [200, 201]:
        return (
            jsonify(
                {
                    "message": "Failed to create exercise (may require admin privileges)",
                    "error": response.json(),
                }
            ),
            response.status_code,
        )

    return jsonify(response.json()), 201


@app.route("/exercises/<int:exercise_id>", methods=["PUT"])
@token_required
def update_exercise(current_user, exercise_id):
    exercise_data = request.json
    access_token, _ = get_wger_access_token()
    if not access_token:
        return jsonify({"message": "Failed to obtain wger access token"}), 500

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    url = f"https://wger.de/api/v2/exercise/{exercise_id}/"
    response = requests.put(url, json=exercise_data, headers=headers)
    if response.status_code not in [200, 202]:
        return (
            jsonify(
                {
                    "message": "Failed to update exercise (may require admin privileges)",
                    "error": response.json(),
                }
            ),
            response.status_code,
        )

    return jsonify(response.json()), 200


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
@token_required
def delete_exercise(current_user, exercise_id):
    access_token, _ = get_wger_access_token()
    if not access_token:
        return jsonify({"message": "Failed to obtain wger access token"}), 500

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://wger.de/api/v2/exercise/{exercise_id}/"
    response = requests.delete(url, headers=headers)
    if response.status_code not in [200, 204, 202]:
        return (
            jsonify(
                {
                    "message": "Failed to delete exercise (may require admin privileges)",
                    "error": response.json(),
                }
            ),
            response.status_code,
        )

    return jsonify({"message": "Exercise deleted successfully"}), 200


# -------------------------------------------------------------------
# Nutritionix API Routes
# -------------------------------------------------------------------
NUTRITIONIX_APP_ID = "a33aca0b"
NUTRITIONIX_APP_KEY = "2bbff0272ab257619aa30f67705b055e"
NUTRITIONIX_BASE_URL = "https://trackapi.nutritionix.com/v2"


@app.route("/nutrition/search", methods=["GET"])
@token_required
def search_food(current_user):
    """
    Searches for foods using Nutritionix's Instant Search endpoint.
    Usage:
      GET /nutrition/search?query=milk
    """
    query = request.args.get("query")
    if not query:
        return jsonify({"message": "Query parameter is required"}), 400

    url = f"{NUTRITIONIX_BASE_URL}/search/instant"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_APP_KEY,
    }
    params = {"query": query}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return (
            jsonify({"message": "Failed to search foods", "error": response.json()}),
            response.status_code,
        )

    return jsonify(response.json()), 200


@app.route("/nutrition/nutrients", methods=["POST"])
@token_required
def get_nutrients_info(current_user):
    """
    Analyzes a food query using Nutritionix's Natural Language endpoint.
    Example JSON body:
    {
      "query": "2 eggs and a slice of bacon"
    }
    """
    data = request.json
    if not data or not data.get("query"):
        return jsonify({"message": "A 'query' field is required in the JSON body"}), 400

    url = f"{NUTRITIONIX_BASE_URL}/natural/nutrients"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_APP_KEY,
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        return (
            jsonify(
                {"message": "Failed to analyze food query", "error": response.json()}
            ),
            response.status_code,
        )

    return jsonify(response.json()), 200
