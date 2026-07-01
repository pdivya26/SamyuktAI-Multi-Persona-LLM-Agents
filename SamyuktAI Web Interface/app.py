from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from groq import Groq
from dotenv import load_dotenv
import os
import requests
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.secret_key="secret_key"
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5000"])

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -----------------------
# Database Initialization
# -----------------------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -----------------------
# Routes
# -----------------------
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                           (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except:
            return "Username already exists"

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            session["user"] = username
            return redirect(url_for("homepage"))
        else:
            return "Invalid credentials"

    return render_template("login.html")

@app.route("/homepage")
def homepage():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("homepage.html", username=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/chat", methods=["POST"])
def chat():
    if "user" not in session:
        return jsonify({"response": "Unauthorized"}), 401

    data = request.json
    prompt = data.get("prompt")
    model_type = data.get("model_type")

    try:
        if model_type == "legal":

            completion = groq_client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Indian legal assistant. Provide brief legal explanations (not too long, not short) and mention IPC sections when relevant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            response = completion.choices[0].message.content

        elif model_type == "medical":

            NGROK_URL = "https://striped-carmelo-unadoringly.ngrok-free.dev/chat"

            try:
                medical_response = requests.post(
                    NGROK_URL,
                    json={"prompt": prompt},
                    timeout=30
                )
                medical_response.raise_for_status()

                response = medical_response.json().get("response", "No response")

            except Exception as e:
                print("NGROK ERROR:", str(e))
                return jsonify({"response": str(e)}), 500

        else:
            response = "Invalid model type selected."

        return jsonify({"response": response})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"response": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
