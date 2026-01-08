from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

@app.route("/")
def health():
    return jsonify({"status": "Backend running"})

@app.route("/db")
def db_check():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return jsonify({"db": "connected"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
