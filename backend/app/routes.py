from datetime import datetime, timedelta
from flask import request, jsonify, make_response
import requests
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
import random

from .models import Users, Funds
from . import app, db


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
        # You can still create a token if you want,
        # but the routes won't require it.
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
# Funds Routes (No user scoping)
# -------------------------------------------------------------------
@app.route("/funds", methods=["GET"])
def get_all_funds():
    """
    Returns ALL funds in the database (not tied to a specific user).
    """
    funds = Funds.query.all()
    total_sum = 0
    if funds:
        total_sum = (
            db.session.query(func.round(func.sum(Funds.amount), 2)).scalar() or 0
        )

    return jsonify({"data": [row.serialize for row in funds], "sum": total_sum})


@app.route("/funds/<id>", methods=["PUT"])
def update_fund(id):
    try:
        fund = Funds.query.filter_by(id=id).first()
        if fund is None:
            return {"message": "Unable to update, fund not found"}, 404

        data = request.json
        amount = data.get("amount")
        if amount is not None:
            try:
                fund.amount = float(amount)
            except ValueError:
                return {"message": "Invalid amount provided"}, 400

        db.session.commit()
        return {"message": fund.serialize}, 200
    except Exception as e:
        print(e)
        return {"error": "Unable to process"}, 409


@app.route("/funds", methods=["POST"])
def post_fund():
    data = request.json
    amount = data.get("amount")
    if amount is None:
        return {"message": "Amount is required"}, 400

    try:
        fund = Funds(amount=float(amount))
        db.session.add(fund)
        db.session.commit()
        return fund.serialize, 201
    except ValueError:
        return {"message": "Invalid amount provided"}, 400
    except Exception as e:
        print(e)
        return {"message": "Unable to create fund"}, 500


@app.route("/funds/<id>", methods=["DELETE"])
def delete_fund(id):
    try:
        fund = Funds.query.filter_by(id=id).first()
        if fund is None:
            return {"message": f"Fund with id {id} not found"}, 404

        db.session.delete(fund)
        db.session.commit()
        return {"message": "Fund deleted successfully"}, 202
    except Exception as e:
        print(e)
        return {"error": "Unable to process"}, 409


# -------------------------------------------------------------------
# Weather Routes using WeatherAPI (No token needed)
# -------------------------------------------------------------------
WEATHER_API_KEY = "d76d4eb38e6d48f1924132518251803"
WEATHER_BASE_URL = "https://api.weatherapi.com/v1"


@app.route("/weather", methods=["GET"])
def get_weather():
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


@app.route("/weather/forecast", methods=["GET"])
def get_weather_forecast():
    location = request.args.get("location")
    days = request.args.get("days", 3)
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


@app.route("/weather/history", methods=["GET"])
def get_weather_history():
    location = request.args.get("location")
    date = request.args.get("date")
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


@app.route("/weather/astronomy", methods=["GET"])
def get_weather_astronomy():
    location = request.args.get("location")
    date = request.args.get("date")
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


@app.route("/weather/timezone", methods=["GET"])
def get_weather_timezone():
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
# Workout / Wger API Routes (No local token, but still uses Wger token)
# -------------------------------------------------------------------
def get_wger_access_token():
    token_url = "https://wger.de/api/v2/token"
    payload = {"username": "lancekian12@gmail.com", "password": "@52425978Qwqw"}
    token_response = requests.post(token_url, data=payload)
    if token_response.status_code != 200:
        return None, token_response.json()
    tokens = token_response.json()
    return tokens.get("access"), tokens.get("refresh")


@app.route("/workouts", methods=["GET"])
def list_workouts():
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


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout_by_id(workout_id):
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


@app.route("/workouts", methods=["POST"])
def create_workout():
    workout_data = request.json
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


@app.route("/workouts/<int:workout_id>", methods=["PUT"])
def update_workout(workout_id):
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


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
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
def list_days():
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
def create_day():
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
def get_day_by_id(day_id):
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
def update_day(day_id):
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
def delete_day(day_id):
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
def list_exercises():
    access_token, _ = get_wger_access_token()
    if not access_token:
        return jsonify({"message": "Failed to obtain wger access token"}), 500

    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://wger.de/api/v2/exercise/"
    response = requests.get(url, headers=headers, params=request.args)
    if response.status_code != 200:
        return (
            jsonify({"message": "Failed to fetch exercises", "error": response.json()}),
            response.status_code,
        )

    return jsonify(response.json()), 200


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise_by_id(exercise_id):
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
def create_exercise():
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
def update_exercise(exercise_id):
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
def delete_exercise(exercise_id):
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


NUTRITIONIX_APP_ID = "a33aca0b"
NUTRITIONIX_APP_KEY = "2bbff0272ab257619aa30f67705b055e"
NUTRITIONIX_BASE_URL = "https://trackapi.nutritionix.com/v2"


@app.route("/calories", methods=["POST"])
def get_nutrition():
    """
    POST /calories
    JSON body: { "query": "2 eggs" }

    Returns the JSON from Nutritionix's /natural/nutrients endpoint.
    """
    data = request.json
    if not data or not data.get("query"):
        return jsonify({"message": "A 'query' field is required in the JSON body"}), 400

    # Build request to Nutritionix
    url = f"{NUTRITIONIX_BASE_URL}/natural/nutrients"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_APP_KEY,
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json={"query": data["query"]})

    if response.status_code != 200:
        return (
            jsonify(
                {"message": "Failed to analyze food query", "error": response.json()}
            ),
            response.status_code,
        )

    # If successful, return the Nutritionix JSON
    return jsonify(response.json()), 200
