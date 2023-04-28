from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
from flask_session import Session
from database import load_job_from_db, load_jobs_from_db, load_business_to_db
from helpers import error, success

def configure():
    load_dotenv()

#application setup
app = Flask(__name__)

#secrete key during deployment
app.secret_key = os.getenv("secrete_key")

# ensuring template autoreloading
app.config["TEMPLATES_ATUO_RELOAD"] = True

# Use filesystem for session instead of signed cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
        return render_template("index.html")

@app.route("/contact-us")
def contact_us():
    return render_template("contact-us.html")

@app.route("/about-us")
def about_us():
    return render_template("about-us.html")

@app.route("/careers")
def careers():
    jobs = load_jobs_from_db()
    return render_template("careers.html", jobs = jobs)

@app.route("/careers/<id>")
def career_detail(id):
    job = load_job_from_db(id)
    return render_template("career-detail.html", job = job)

@app.route("/success")
def success():
    job = load_jobs_from_db()
    return render_template("success.html", output = job)

@app.route("/api/jobs")
def list_jobs():
    return jsonify(JOBS)

@app.route("/business")
def business():
    return render_template("business.html")

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/terms-and-conditions")
def terms_and_conditions():
    return render_template("terms-and-conditions.html")

@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy-policy.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/forgot-username")
def forgot_username():
    return render_template("forgot-username.html")

@app.route("/login-continue")
def continue_login():
    return render_template("login-continue.html")