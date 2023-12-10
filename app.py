import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import json


import re

from helpers import login_required, validate_ad_type, get_non_empty_fields

MAX_TITLE_LENGTH = 60
MAX_DESCRYPTION_LENGTH = 200

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

@app.before_request
def before_request():
    g.display_username = None  

    if "user_id" in session:
        user_id = session["user_id"]
        result = db.execute("SELECT username FROM autenticacao WHERE id = ?", (user_id,))
        g.display_username = result[0]["username"] if result else None




@app.route('/', methods=['GET', 'POST'])
def index():
    if "user_id" in session:
        user_id = session["user_id"]
        
        result = db.execute("SELECT username FROM autenticacao WHERE id = ?", (user_id,))
        display_username = result[0]["username"] if result else None
        return render_template("index.html", display_username=display_username)

    return render_template("index.html")


#Login routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect("/")
    
    if request.method == 'GET':
        return render_template("login.html")
    
    error_message = None
    username_input = request.form.get("username")
    password_input = request.form.get("password")

    if not username_input or not password_input:
        error_message = "403 - You must provide a username and password"
    else:
        rows = db.execute("SELECT * FROM autenticacao WHERE username = ?", username_input)
        
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password_input):
            error_message = "403 - Authentication Failed: The provided username does not exist or the password is incorrect"
        else:
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            # Redirect user to home page
            return redirect("/")
    
    return render_template("login.html", error=error_message)

        

from flask import render_template

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

    error_message = None
    message = None

    try:
        # Validation queries
        validation_username = db.execute("SELECT * FROM autenticacao WHERE username = ?", username_input)
        validation_email = db.execute("SELECT * FROM autenticacao WHERE email = ?", email_input)

        # Check if username or email is already in use
        if len(validation_username) == 1:
            error_message = "403 - This username is already in use"
            user_isvalid = False

        elif len(validation_email) == 1:
            error_message = "403 - This email is already in use"
            user_isvalid = False

        # Check for empty fields
        if not username_input or not password_input or not confirm_input or not email_input:
            error_message = "403 - Please fill in all the fields"
            user_isvalid = False

        if password_input != confirm_input:
            error_message = "403 - Passwords must be identical"
            user_isvalid = False

        if not (
            re.search(r"[a-zA-Z]", password_input)
            and re.search(r"\d", password_input)
            and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password_input)
        ):
            error_message = "403 - Password must contain at least one letter, one digit, and one special character"
            user_isvalid = False

        # Hashing password and adding to the database only if all validations pass
        if user_isvalid:
            password_hashed = generate_password_hash(password_input)
            db.execute("INSERT INTO autenticacao (username, password, email) VALUES (?, ?, ?)", username_input, password_hashed, email_input)

            # Registration successful
            message ="Registration successful"
            return render_template("login.html", message= message )

    except Exception as e:

        error_message = "500 - Internal Server Error"

    # Render the template com a mensagem de erro
    return render_template("register.html", error=error_message)



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
@app.route("/announce", methods=["GET", "POST"])
@login_required
def announce():
    error_message = None

    if request.method == "GET":
        return render_template("announce.html")

    if request.method == "POST":
        ad_type_return = request.form.get("ad_category")

        ad_types_allowed = ['houses_Ad', "ownedCars_Ad", "furniture_Ad", "tech_Ad", "musical_Ad", "toys_Ad", "pet_Ad", "office_Ad", "fashion_Ad", "games_Ad"]
        
        if ad_type_return not in ad_types_allowed:
            error_message = "400 - Ad_type_notAllowed"
        else:
            return render_template("AdsCreate.html", ads_type=ad_type_return)

    return render_template("announce.html", error=error_message)




@app.route("/adsCreate", methods=['POST'])
@login_required
def adCreationDB():
    hidden_type = request.form.get('ads_type')
    user_onSection = session.get('user_id')
    error_message = None

    if validate_ad_type(hidden_type) and user_onSection:
        form_fields = get_non_empty_fields(
            request,
            'title', 'description', 'firstDataList', 'secondDataList',
            'thirdDataList', 'forthDataList', 'tirthForm', 'forthForm', 'fifthForm',
            'sixthForm', 'rentOrSellchecklist', 'checkList'
        )

        type_mapping = {
            'houses_Ad': 'RealState',
            'ownedCars_Ad': 'PreOwnedCars',
            'furniture_Ad': 'HomeEssentials',
            'tech_Ad': 'TechEssentials',
            'musical_Ad': 'MusicalInstrument',
            'toys_Ad': 'Children_Items_Toys',
            'pet_Ad': 'Pets',
            'office_Ad': 'Commerce_office',
            'fashion_Ad': 'Fashion_Beauty',
            'games_Ad': 'Games'
        }

        convert_type = type_mapping.get(hidden_type, None)

        if convert_type:
            # Inserir anúncio na tabela announces
            db.execute(
                'INSERT INTO announces (title, description, announcement_type, user_id) VALUES (?, ?, ?, ?)',
                form_fields['title'], form_fields['description'], convert_type, user_onSection
            )

            result = db.execute('SELECT id FROM announces ORDER BY id DESC LIMIT 1')
            announce_id = result[0]['id'] if result else None

            if announce_id is not None:
                
                principal_checklist_values = request.form.getlist('principalCheckList')
                principal_checklist_json = json.dumps(principal_checklist_values)
                print("Principal Checklist Values:", principal_checklist_values)

                match convert_type:
                    case 'RealState':
                        db.execute(
                            'INSERT INTO RealState (PropertyType, RentSale, NumberOfRooms, NumberOfBathrooms, AreaM2, GarageSpace, DependenciesID, Price, ImagesID, Address, Contact, announce_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            form_fields['firstDataList'], form_fields['rentOrSellchecklist'], form_fields['secondDataList'],
                            form_fields['thirdDataList'], form_fields['tirthForm'], form_fields['forthDataList'],
                            principal_checklist_json, form_fields['forthForm'],
                            None, form_fields['fifthForm'], form_fields['sixthForm'], announce_id
                        )

                    case 'PreOwnedCars':
                        db.execute(
                            'INSERT INTO PreOwnedCars(CarModel, RentSale, Transmission, Engine, Mileage, Doors, CarAtributtes, Price, ImagesID, Address, Contact, announce_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            form_fields['firstDataList'], form_fields['rentOrSellchecklist'], form_fields['secondDataList'],
                            form_fields['thirdDataList'], form_fields['tirthForm'], form_fields['forthDataList'],
                            principal_checklist_json, form_fields['forthForm'],
                            None, form_fields['fifthForm'], form_fields['sixthForm'], announce_id
                        )

                    case 'HomeEssentials':
                        db.execute(
                            'INSERT INTO HomeEssentials(Categorys, Conditions, Price, ImagesID, Address, Contact, announce_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                            form_fields['firstDataList'], form_fields['secondDataList'],
                            form_fields['forthForm'], None, form_fields['fifthForm'], form_fields['sixthForm'], announce_id
                        )

                    case 'TechEssentials':
                        db.execute(
                            'INSERT INTO TechEssentials(Type, Model, Conditions, Price, ImagesID, Address, Contact, announce_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                            form_fields['firstDataList'], form_fields['secondDataList'], form_fields['thirdDataList'],
                            form_fields['forthForm'], None, form_fields['fifthForm'], form_fields['sixthForm'], announce_id
                        )

                    case 'MusicalInstrument':
                        db.execute(
                            'INSERT INTO MusicalInstrument(Type, Model, Conditions, Price, ImagesID, Address, Contact, announce_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                            form_fields['firstDataList'], form_fields['secondDataList'], form_fields['thirdDataList'],
                            form_fields['forthForm'], None, form_fields['fifthForm'], form_fields['sixthForm'], announce_id
                        )

                    case 'Children_Items_Toys':
                        db.execute(
                            'INSERT INTO Children_Items_Toys(Type, Conditions, Price, ImagesID, Address, Contact, announce_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                            form_fields['firstDataList'], form_fields['secondDataList'], form_fields['forthForm'], None, form_fields['fifthForm'], form_fields['sixthForm'], announce_id
                        )

                    case 'Pets':
                        db.execute(
                            'INSERT INTO Pets(Type, Conditions, Price, ImagesID, Address, Contact, announce_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                            form_fields['firstDataList'], form_fields['secondDataList'], form_fields['forthForm'], None, form_fields['fifthForm'], form_fields['sixthForm'], announce_id
                        )

                    case 'Commerce_office':
                        db.execute(
                            'INSERT INTO Commerce_office( Price, ImagesID, Address, Contact, announce_id) VALUES ( ?, ?, ?, ?, ?)',
                            form_fields['forthForm'], None, form_fields['fifthForm'], form_fields['sixthForm'], announce_id
                        )

                    case 'Fashion_Beauty':
                        db.execute(
                            'INSERT INTO Fashion_Beauty(Type, Price, ImagesID, Address, Contact, announce_id) VALUES ( ?, ?, ?, ?, ?, ?)',
                            form_fields['firstDataList'], form_fields['forthForm'], None, form_fields['fifthForm'], form_fields['sixthForm'], announce_id
                        )

                    case 'Games':
                        db.execute(
                            'INSERT INTO Games(Type, Conditions, Price, ImagesID, Address, Contact, announce_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                            form_fields['firstDataList'], form_fields['secondDataList'], form_fields['forthForm'], None, form_fields['fifthForm'], form_fields['sixthForm'], announce_id
                        )

                flash("Announce Create Sucessifuly")
                return redirect('/')
                    
    return render_template("AdsCreate.html", error=error_message)


               