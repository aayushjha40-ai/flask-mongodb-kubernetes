from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# Read MongoDB URI from environment variable
MONGO_URI = os.environ.get("MONGODB_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.flask_db
collection = db.data


@app.route("/")
def index():
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"


@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        collection.insert_one(request.json)
        return {"status": "Data inserted"}, 201
    else:
        return jsonify(list(collection.find({}, {"_id": 0})))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
