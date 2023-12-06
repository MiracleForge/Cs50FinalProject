import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, get_flashed_messages
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

import re

from helpers import login_required
app = Flask(__name__) 

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///app_db.db")

# Config cache 
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    if "user_id" in session:
        user_id = session["user_id"]
        
        result = db.execute("SELECT username FROM autenticacao WHERE id = ?", (user_id,))
        display_username = result[0]["username"] if result else None
        return render_template("layout.html", display_username=display_username)

    return render_template("layout.html")

#Login routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect("/")
    
    if request.method == 'GET':

        return render_template("login.html")
    
    username_input = request.form.get("username")
    password_input = request.form.get("password")

    if not username_input or not password_input:
        flash("You must provide a username and password", 403)
        return render_template("login.html")
    
    rows = db.execute(
        "SELECT * FROM autenticacao WHERE username = ?", username_input
        )
    
     # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(
        rows[0]["password"], password_input
    ):
        return render_template("login.html")
    
    # Remember which user has logged in
    session["user_id"] = rows[0]["id"]

    # Redirect user to home page
    return redirect("/")
        

@app.route("/register", methods=["GET", "POST"])
def register():

    if "user_id" in session:
        return redirect("/")
    
    if request.method == 'GET':
        return render_template("register.html")

    # Inputs from the form
    username_input = request.form.get("username")
    password_input = request.form.get("password")
    confirm_input = request.form.get("confirmPassword")
    email_input = request.form.get("email")
    user_isvalid = True

    # Validation queries
    validation_username = db.execute("SELECT * FROM autenticacao WHERE username = ?", username_input)
    validation_email = db.execute("SELECT * FROM autenticacao WHERE email = ?", email_input)

    # Check if username or email is already in use
    if len(validation_username) == 1:
        flash("This username is already in use", "error")
        user_isvalid = False

    elif len(validation_email) == 1:
        flash("This email is already in use", "error")
        user_isvalid = False

    # Check for empty fields
    if not username_input or not password_input or not confirm_input or not email_input:
        flash("Please fill in all the fields", "error")
        user_isvalid = False


    if password_input != confirm_input:
        flash("Passwords must be identical", "error")
        user_isvalid = False


    if not (
            re.search(r"[a-zA-Z]", password_input)
            and re.search(r"\d", password_input)
            and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password_input)
        ):
        flash("Password must contain at least one letter, one digit, and one special character", "error")
        user_isvalid = False
    
    #Hashing password
    if user_isvalid:
        password_hashed = generate_password_hash(password_input)

        # UPDATING DATABASE
        db.execute("INSERT INTO autenticacao (username, password, email) VALUES (?, ?, ?)", username_input, password_hashed, email_input)

        # Registration successful
        flash("Registration successful!", "success")
        return redirect("/login")
    else:
        
        return redirect("/register")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


#NAV ROUTES
@app.route("/myads", methods=["GET"])
def myads():
    if request.method == 'GET':
        if "user_id" in session:
            return redirect("/")
        else:
            return render_template("login.html")
        
#trying to work with git
@app.route("/announce", methods = ["GET", "POST"])
@login_required
def announce():
    if request.method == "GET":
        return render_template("announce.html")
    
    if request.method == "POST":
        ad_type_return = request.form.get("ad_category")

        if not ad_type_return:
            return render_template("announce.html")

        return render_template("AdsCreate.html", ads_type=ad_type_return)




