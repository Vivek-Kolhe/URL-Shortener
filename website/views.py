import re
import random
import string
from . import db
from .models import URL_DB
from flask import Blueprint, render_template, request, redirect, flash

URL_REGEX = (
            "((http|https)://)(www.)?" +
            "[a-zA-Z0-9@:%._\\+~#?&//=]" +
            "{2,256}\\.[a-z]" +
            "{2,6}\\b([-a-zA-Z0-9@:%" +
            "._\\+~#?&//=]*)"
            )
REGEX = re.compile(URL_REGEX)

views = Blueprint("views", __name__)

@views.route('/', methods = ["POST", "GET"])
def home():
    if request.method == "POST":
        _long_url = request.form.get("urlInput")
        custom_name = request.form.get("customName")

        if not re.search(REGEX, _long_url):
            flash(f"Entered URL is invalid! Try again!", category = "error")
        else:
            if custom_name == "":
                custom_name = "".join(random.choices(string.ascii_lowercase + string.digits, k = 6))
            
            short_url = f"https://makemeshort.com/{custom_name}"
            put_db = URL_DB(long_url = _long_url, short_url = short_url, visits = 0, ip_address = request.remote_addr)
            db.session.add(put_db)
            db.session.commit()
            return render_template("home.html", short_url = short_url)
    return render_template("home.html")

@views.route('/analytics')
def analytics():
    all_queries = URL_DB.query.all()
    return render_template("analytics.html", all_queries = all_queries)
