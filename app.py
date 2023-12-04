#Import components for the API
from flask import Flask, flash,  render_template, request, redirect, session
from flask_session import Session
#import db components
from cs50 import SQL

app = Flask(__name__) 
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#db = SQL("sqlite3:///app_db.db")
# Config cache 
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/', methods = ['GET', 'POST'])
def index():
    
    return render_template("layout.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':

        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':

        return render_template("register.html")
    