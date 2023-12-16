from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, g
from flask_session import Session
from functools import wraps

from PIL import Image  
from io import BytesIO
import base64 #converting back to base64

MAX_TITLE_LENGTH = 60
MAX_DESCRYPTION_LENGTH = 200


# working with git
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



def get_non_empty_fields(request, *field_names):
    """
    Retorna um dicionário contendo os campos preenchidos e que não contenham apenas espaços em branco.

    Parameters:
    - request: Objeto de requisição Flask
    - field_names: Nomes dos campos a serem verificados

    Returns:
    - Um dicionário contendo os campos não vazios
    """
    non_empty_fields = {}
    for field_name in field_names:
        values = request.form.getlist(field_name)
        non_empty_values = [value for value in values if value and value.strip()]
        if non_empty_values:
            non_empty_fields[field_name] = non_empty_values
    return non_empty_fields


def validate_ad_type(ad_type):
    
    ad_types_allowed = ['houses_Ad', "ownedCars_Ad", "furniture_Ad", "tech_Ad", "musical_Ad", "toys_Ad", "pet_Ad", "office_Ad", "fashion_Ad", "games_Ad"]
    if ad_type not in ad_types_allowed:
        return False, "Ad_type not allowed"
    return True

















    





                    


