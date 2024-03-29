import os
#Basic for the app
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, g, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import json
#for converting blob to png
from PIL import Image  
from io import BytesIO
import base64 #converting back to base64
# To password 
import re


from helpers import login_required, validate_ad_type, get_non_empty_fields, convert_blob_to_png

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
    if request.method == "GET":
        dataReal = db.execute(
            "SELECT announces.id, announces.title, RealState.Price AS price, AnnounceImages.image_data, RealState.Address AS address "
            "FROM announces "
            "LEFT JOIN RealState ON RealState.announce_id = announces.id AND announces.announcement_type = 'RealState' "
            "LEFT JOIN AnnounceImages ON AnnounceImages.announce_id = announces.id "
            "WHERE announces.announcement_type = 'RealState' "
            "LIMIT 16;"
        )

        dataCars = db.execute(
            "SELECT announces.id, announces.title, PreOwnedCars.Price AS price, AnnounceImages.image_data, PreOwnedCars.Address AS address "
            "FROM announces "
            "LEFT JOIN PreOwnedCars ON PreOwnedCars.announce_id = announces.id AND announces.announcement_type = 'PreOwnedCars' "
            "LEFT JOIN AnnounceImages ON AnnounceImages.announce_id = announces.id "
            "WHERE announces.announcement_type = 'PreOwnedCars' "
            "LIMIT 16;"
        )

        for ad in dataCars:
                if ad["image_data"]:
                    ad["image_data"] = convert_blob_to_png(ad["image_data"])

        for ad in dataReal:
                if ad["image_data"]:
                    ad["image_data"] = convert_blob_to_png(ad["image_data"])

        return render_template("index.html", dataReal=dataReal, dataCars=dataCars)


@app.route("/filtered_ads", methods=['POST'])
def filtered_Ads():
    menu_indexFilter = None
    search_query = request.form.get('search_query')

    if request.form.get("filtered_ads") or request.form.get("promotionTech"):
        
        if request.form.get('filtered_ads') == 'TVs':
            seach_filter = db.execute("""
                SELECT
                    announces.id,
                    announces.title,
                    TechEssentials.Price AS price,
                    TechEssentials.Address AS address,
                    AnnounceImages.image_data
                FROM
                    announces
                LEFT JOIN
                    TechEssentials ON TechEssentials.announce_id = announces.id AND announces.announcement_type = 'TechEssentials'
                LEFT JOIN
                    AnnounceImages ON AnnounceImages.announce_id = announces.id
                WHERE
                    announces.announcement_type = 'TechEssentials'
                    AND TechEssentials.Type = ?;

                """, (request.form.get('filtered_ads'),))
            menu_indexFilter = 'Tech Essentials'
        elif request.form.get('filtered_ads') == 'promotionTech':
            
            seach_filter = db.execute("""
                SELECT
                    announces.id,
                    announces.title,
                    TechEssentials.Price AS price,
                    TechEssentials.Address AS address,
                    AnnounceImages.image_data
                FROM
                    announces
                LEFT JOIN
                    TechEssentials ON TechEssentials.announce_id = announces.id AND announces.announcement_type = 'TechEssentials'
                LEFT JOIN
                    AnnounceImages ON AnnounceImages.announce_id = announces.id
                WHERE
                    announces.announcement_type = 'TechEssentials'
                    AND (
                        announces.title LIKE '%promotion%'
                        OR announces.title LIKE '%discount%'
                        OR announces.title LIKE '%off%'
           
                    );
            """)
            menu_indexFilter = 'Tech Off'

        else:
            menu_indexFilter = request.form.get("filtered_ads")
            seach_filter = db.execute(
                "SELECT announces.id, announces.title, "
                "CASE "
                "   WHEN announces.announcement_type = 'PreOwnedCars' THEN PreOwnedCars.Price "
                "   WHEN announces.announcement_type = 'RealState' THEN RealState.Price "
                "   WHEN announces.announcement_type = 'HomeEssentials' THEN HomeEssentials.Price "
                "   WHEN announces.announcement_type = 'TechEssentials' THEN TechEssentials.Price "
                "   WHEN announces.announcement_type = 'MusicalInstrument' THEN MusicalInstrument.Price "
                "   WHEN announces.announcement_type = 'Children_Items_Toys' THEN Children_Items_Toys.Price "
                "   WHEN announces.announcement_type = 'Pets' THEN Pets.Price "
                "   WHEN announces.announcement_type = 'Commerce_office' THEN Commerce_office.Price "
                "   WHEN announces.announcement_type = 'Fashion_Beauty' THEN Fashion_Beauty.Price "
                "   WHEN announces.announcement_type = 'Games' THEN Games.Price "
                "END AS price, "
                "CASE "
                "   WHEN announces.announcement_type = 'PreOwnedCars' THEN PreOwnedCars.Address "
                "   WHEN announces.announcement_type = 'RealState' THEN RealState.Address "
                "   WHEN announces.announcement_type = 'HomeEssentials' THEN HomeEssentials.Address "
                "   WHEN announces.announcement_type = 'TechEssentials' THEN TechEssentials.Address "
                "   WHEN announces.announcement_type = 'MusicalInstrument' THEN MusicalInstrument.Address "
                "   WHEN announces.announcement_type = 'Children_Items_Toys' THEN Children_Items_Toys.Address "
                "   WHEN announces.announcement_type = 'Pets' THEN Pets.Address "
                "   WHEN announces.announcement_type = 'Commerce_office' THEN Commerce_office.Address "
                "   WHEN announces.announcement_type = 'Fashion_Beauty' THEN Fashion_Beauty.Address "
                "   WHEN announces.announcement_type = 'Games' THEN Games.Address "
                "END AS address, "
                "AnnounceImages.image_data "
                "FROM announces "
                "LEFT JOIN PreOwnedCars ON PreOwnedCars.announce_id = announces.id AND announces.announcement_type = 'PreOwnedCars' "
                "LEFT JOIN RealState ON RealState.announce_id = announces.id AND announces.announcement_type = 'RealState' "
                "LEFT JOIN HomeEssentials ON HomeEssentials.announce_id = announces.id AND announces.announcement_type = 'HomeEssentials' "
                "LEFT JOIN TechEssentials ON TechEssentials.announce_id = announces.id AND announces.announcement_type = 'TechEssentials' "
                "LEFT JOIN MusicalInstrument ON MusicalInstrument.announce_id = announces.id AND announces.announcement_type = 'MusicalInstrument' "
                "LEFT JOIN Children_Items_Toys ON Children_Items_Toys.announce_id = announces.id AND announces.announcement_type = 'Children_Items_Toys' "
                "LEFT JOIN Pets ON Pets.announce_id = announces.id AND announces.announcement_type = 'Pets' "
                "LEFT JOIN Commerce_office ON Commerce_office.announce_id = announces.id AND announces.announcement_type = 'Commerce_office' "
                "LEFT JOIN Fashion_Beauty ON Fashion_Beauty.announce_id = announces.id AND announces.announcement_type = 'Fashion_Beauty' "
                "LEFT JOIN Games ON Games.announce_id = announces.id AND announces.announcement_type = 'Games' "
                "LEFT JOIN AnnounceImages ON AnnounceImages.announce_id = announces.id "
                "WHERE announces.announcement_type = ?;",
                (menu_indexFilter,)
            )

        for ad in seach_filter:
            if ad["image_data"]:
                ad["image_data"] = convert_blob_to_png(ad["image_data"])
          
        return render_template("index_filteredAds.html", menu_indexFilter=menu_indexFilter, seach_filter=seach_filter)
    #search form layout
    if search_query:
        query_pattern = f"%{search_query}%"

        seach_filter = db.execute(
            f"SELECT announces.id, announces.title, "
            f"CASE "
            f"   WHEN announces.announcement_type = 'PreOwnedCars' THEN PreOwnedCars.Price "
            f"   WHEN announces.announcement_type = 'RealState' THEN RealState.Price "
            f"   WHEN announces.announcement_type = 'HomeEssentials' THEN HomeEssentials.Price "
            f"   WHEN announces.announcement_type = 'TechEssentials' THEN TechEssentials.Price "
            f"   WHEN announces.announcement_type = 'MusicalInstrument' THEN MusicalInstrument.Price "
            f"   WHEN announces.announcement_type = 'Children_Items_Toys' THEN Children_Items_Toys.Price "
            f"   WHEN announces.announcement_type = 'Pets' THEN Pets.Price "
            f"   WHEN announces.announcement_type = 'Commerce_office' THEN Commerce_office.Price "
            f"   WHEN announces.announcement_type = 'Fashion_Beauty' THEN Fashion_Beauty.Price "
            f"   WHEN announces.announcement_type = 'Games' THEN Games.Price "
            f"END AS price, "
            f"CASE "
            f"   WHEN announces.announcement_type = 'PreOwnedCars' THEN PreOwnedCars.Address "
            f"   WHEN announces.announcement_type = 'RealState' THEN RealState.Address "
            f"   WHEN announces.announcement_type = 'HomeEssentials' THEN HomeEssentials.Address "
            f"   WHEN announces.announcement_type = 'TechEssentials' THEN TechEssentials.Address "
            f"   WHEN announces.announcement_type = 'MusicalInstrument' THEN MusicalInstrument.Address "
            f"   WHEN announces.announcement_type = 'Children_Items_Toys' THEN Children_Items_Toys.Address "
            f"   WHEN announces.announcement_type = 'Pets' THEN Pets.Address "
            f"   WHEN announces.announcement_type = 'Commerce_office' THEN Commerce_office.Address "
            f"   WHEN announces.announcement_type = 'Fashion_Beauty' THEN Fashion_Beauty.Address "
            f"   WHEN announces.announcement_type = 'Games' THEN Games.Address "
            f"END AS address, "
            f"AnnounceImages.image_data "
            f"FROM announces "
            f"LEFT JOIN PreOwnedCars ON PreOwnedCars.announce_id = announces.id AND announces.announcement_type = 'PreOwnedCars' "
            f"LEFT JOIN RealState ON RealState.announce_id = announces.id AND announces.announcement_type = 'RealState' "
            f"LEFT JOIN HomeEssentials ON HomeEssentials.announce_id = announces.id AND announces.announcement_type = 'HomeEssentials' "
            f"LEFT JOIN TechEssentials ON TechEssentials.announce_id = announces.id AND announces.announcement_type = 'TechEssentials' "
            f"LEFT JOIN MusicalInstrument ON MusicalInstrument.announce_id = announces.id AND announces.announcement_type = 'MusicalInstrument' "
            f"LEFT JOIN Children_Items_Toys ON Children_Items_Toys.announce_id = announces.id AND announces.announcement_type = 'Children_Items_Toys' "
            f"LEFT JOIN Pets ON Pets.announce_id = announces.id AND announces.announcement_type = 'Pets' "
            f"LEFT JOIN Commerce_office ON Commerce_office.announce_id = announces.id AND announces.announcement_type = 'Commerce_office' "
            f"LEFT JOIN Fashion_Beauty ON Fashion_Beauty.announce_id = announces.id AND announces.announcement_type = 'Fashion_Beauty' "
            f"LEFT JOIN Games ON Games.announce_id = announces.id AND announces.announcement_type = 'Games' "
            f"LEFT JOIN AnnounceImages ON AnnounceImages.announce_id = announces.id "
            f"WHERE announces.title LIKE '{query_pattern}' OR announces.description LIKE '{query_pattern}' "
            f"OR PreOwnedCars.CarModel LIKE '{query_pattern}' OR RealState.PropertyType LIKE '{query_pattern}' "
            f"OR HomeEssentials.Categorys LIKE '{query_pattern}' OR TechEssentials.Type LIKE '{query_pattern}' "
            f"OR MusicalInstrument.Type LIKE '{query_pattern}' OR Children_Items_Toys.Type LIKE '{query_pattern}' "
            f"OR Pets.Type LIKE '{query_pattern}' OR Commerce_office.Address LIKE '{query_pattern}' "
            f"OR Fashion_Beauty.Type LIKE '{query_pattern}' OR Games.Type LIKE '{query_pattern}';"
        )

        if not seach_filter:
            return render_template("index_filteredAds.html", seach_filter=seach_filter, search_query=search_query)
    
        for ad in seach_filter:
            if ad["image_data"]:
                ad["image_data"] = convert_blob_to_png(ad["image_data"])

        return render_template("index_filteredAds.html", seach_filter=seach_filter, search_query=search_query)


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
@app.route("/myads", methods=['GET', 'POST'])
@login_required
def ShowingUserAds():
    if request.method == "GET":
        if "user_id" in session:
            user_id = session["user_id"]
            # Executar a consulta e obter os resultados
            user_ads = db.execute(
                "SELECT announces.id, announces.title, "
                "CASE "
                "   WHEN announces.announcement_type = 'PreOwnedCars' THEN PreOwnedCars.Price "
                "   WHEN announces.announcement_type = 'RealState' THEN RealState.Price "
                "   WHEN announces.announcement_type = 'HomeEssentials' THEN HomeEssentials.Price "
                "   WHEN announces.announcement_type = 'TechEssentials' THEN TechEssentials.Price "
                "   WHEN announces.announcement_type = 'MusicalInstrument' THEN MusicalInstrument.Price "
                "   WHEN announces.announcement_type = 'Children_Items_Toys' THEN Children_Items_Toys.Price "
                "   WHEN announces.announcement_type = 'Pets' THEN Pets.Price "
                "   WHEN announces.announcement_type = 'Commerce_office' THEN Commerce_office.Price "
                "   WHEN announces.announcement_type = 'Fashion_Beauty' THEN Fashion_Beauty.Price "
                "   WHEN announces.announcement_type = 'Games' THEN Games.Price "
                "END AS price, "
                "AnnounceImages.image_data "
                "FROM announces "
                "LEFT JOIN PreOwnedCars ON PreOwnedCars.announce_id = announces.id AND announces.announcement_type = 'PreOwnedCars' "
                "LEFT JOIN RealState ON RealState.announce_id = announces.id AND announces.announcement_type = 'RealState' "
                "LEFT JOIN HomeEssentials ON HomeEssentials.announce_id = announces.id AND announces.announcement_type = 'HomeEssentials' "
                "LEFT JOIN TechEssentials ON TechEssentials.announce_id = announces.id AND announces.announcement_type = 'TechEssentials' "
                "LEFT JOIN MusicalInstrument ON MusicalInstrument.announce_id = announces.id AND announces.announcement_type = 'MusicalInstrument' "
                "LEFT JOIN Children_Items_Toys ON Children_Items_Toys.announce_id = announces.id AND announces.announcement_type = 'Children_Items_Toys' "
                "LEFT JOIN Pets ON Pets.announce_id = announces.id AND announces.announcement_type = 'Pets' "
                "LEFT JOIN Commerce_office ON Commerce_office.announce_id = announces.id AND announces.announcement_type = 'Commerce_office' "
                "LEFT JOIN Fashion_Beauty ON Fashion_Beauty.announce_id = announces.id AND announces.announcement_type = 'Fashion_Beauty' "
                "LEFT JOIN Games ON Games.announce_id = announces.id AND announces.announcement_type = 'Games' "
                "LEFT JOIN AnnounceImages ON AnnounceImages.announce_id = announces.id "
                "WHERE announces.user_id = ?;",
                user_id)


     
            for ad in user_ads:
                    if ad["image_data"]:
                        ad["image_data"] = convert_blob_to_png(ad["image_data"])

            return render_template("Myads.html", user_ads=user_ads)
    else:

        id_announce = request.form.get("id_announce")
        # get the username
        announce_owner_query = "SELECT a.user_id, u.username FROM announces a JOIN autenticacao u ON a.user_id = u.id WHERE a.id = ?"
        result_announce_owner = db.execute(announce_owner_query, id_announce)

        for row in result_announce_owner:
            user_id = row.get("user_id")
            username = row.get("username")
        # get the announce 
        announce_data = db.execute("SELECT * FROM announces WHERE id =?", id_announce
            )

        imagem_ads = db.execute("SELECT image_data FROM AnnounceImages WHERE announce_id =?", id_announce)
        
        for ad in imagem_ads:
                if ad["image_data"]:
                    ad["image_data"] = convert_blob_to_png(ad["image_data"])

        temp = announce_data[0]
        announce_type = temp['announcement_type']
        json_data_list = None
        match announce_type:
            case 'RealState':
                info_data = db.execute("SELECT * FROM RealState WHERE announce_id =?", id_announce)
                json_data_list = []

                for json_data in info_data:
                    json_data['DependenciesID'] = json.loads(json_data['DependenciesID'])
                    json_data_list.append(json_data)

            case 'PreOwnedCars':
                info_data = db.execute("SELECT * FROM PreOwnedCars WHERE announce_id =?", id_announce)
                json_data_list = []

                for json_data in info_data:
                    json_data['CarAtributtes'] = json.loads(json_data['CarAtributtes'])
                    json_data_list.append(json_data)

            case 'HomeEssentials':
                info_data = db.execute("SELECT * FROM HomeEssentials WHERE announce_id =?", id_announce)
            
            case 'TechEssentials':
                info_data = db.execute("SELECT * FROM TechEssentials WHERE announce_id =?", id_announce)
            
            case 'MusicalInstrument':
                info_data = db.execute("SELECT * FROM MusicalInstrument WHERE announce_id =?", id_announce)
            
            case 'Pets':
                info_data = db.execute("SELECT * FROM Pets WHERE announce_id =?", id_announce)
            
            case 'Children_Items_Toys':
                info_data = db.execute("SELECT * FROM Children_Items_Toys WHERE announce_id =?", id_announce)
            
            case 'Commerce_office':
                info_data = db.execute("SELECT * FROM Commerce_office WHERE announce_id =?", id_announce)
            
            case 'Fashion_Beauty':
                info_data = db.execute("SELECT * FROM Fashion_Beauty WHERE announce_id =?", id_announce)
            
            case 'Games':
                info_data = db.execute("SELECT * FROM Games WHERE announce_id =?", id_announce)
       
        return render_template("renderUserAD.html",owner_ad_data=username, announce_data=announce_data, image_data=imagem_ads, info_data=info_data, json_data_list=json_data_list, id_announce=id_announce)

        
        
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

            for file in request.files.getlist('files'):
                print(f"Processing file: {file.filename}")
                image_data = file.read()
                print(f"Image data: {image_data[:50]}...") 
                db.execute("INSERT INTO AnnounceImages(announce_id, image_data, user_id) VALUES (?, ?, ?)",
                        announce_id, image_data, user_onSection)
            if announce_id is not None:
                
                principal_checklist_values = request.form.getlist('principalCheckList')
                principal_checklist_json = json.dumps(principal_checklist_values)

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


@app.route("/chat", methods=['GET', 'POST'])
@login_required
def user_chat():
    user_id = session["user_id"]
    new_chat = request.args.get("openChat")
    id_announce = request.args.get("id_announce")
    announce_data = None
    message_data = None
    # Redirection requests
    if request.method == 'GET':
        if not new_chat:
            new_chat = False
        else:
            query = """
                SELECT
                    a.id as announce_id,
                    a.title,
                    ai.image_data,
                    a.user_id as announce_user_id,
                    u.username as announce_username
                FROM
                    announces a
                JOIN
                    AnnounceImages ai ON a.id = ai.announce_id
                JOIN
                    autenticacao u ON a.user_id = u.id
                WHERE
                    a.id = ?
            """

            message_data = db.execute("SELECT * FROM Chat WHERE sender_user_id =? AND announce_id =?", user_id, id_announce)
            announce_data = db.execute(query, id_announce)

            for ad in announce_data:
                if ad["image_data"]:
                    ad["image_data"] = convert_blob_to_png(ad["image_data"])

        return render_template("chat.html", sender_messages=message_data, new_chat=new_chat, announce_data=announce_data)
    else:
        message_text = request.form.get('message_action')
        id_announce = int(request.form.get('announce_id'))
        receiver_username = request.form.get('receiver_user_id')


        receiver = db.execute("SELECT id FROM autenticacao WHERE username = ?", (receiver_username,))

        for row in receiver:
            receiver_id = row.get("id")

        print(user_id, receiver_id, id_announce, message_text)

        db.execute("INSERT INTO Chat (sender_user_id, receiver_user_id, announce_id, message_text) VALUES ({}, {}, {}, '{}')".format(user_id, receiver_id, id_announce, message_text))



        return redirect("/chat")




