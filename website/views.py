import re
import random
import string
from . import db
from .models import URL_DB
from flask import Blueprint, render_template, request, redirect, flash, abort, jsonify

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
            # checking if the given url is valid
            flash(f"Entered URL is invalid! Try again!", category = "error")
        else:
            if custom_name == "":
                # generating random endpoint for the short url, if isn't specified by the user.
                custom_name = "".join(random.choices(string.ascii_lowercase + string.digits, k = 6))
            
            check_long_url = URL_DB.query.filter_by(long_url = _long_url).first()
            if check_long_url:
                # checking if the given long url exists in the database.
                flash("Entered long URL already exists in the database. Serving the existing short URL.", category = "error")
                return render_template("home.html", short_url = check_long_url.short_url)

            if custom_name:
                # checking if the endpoint already exists in the database.
                check_custom_name = URL_DB.query.filter_by(short_url = f"https://makemeshort.com/{custom_name}").first()
                if check_custom_name:
                    flash("Custom name already exists. Try again!", category = "error")
                    return render_template("home.html")

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

@views.route('/<endpoint>')
def redirection_to_page(endpoint):
    # checking endpoints, if it exists in the database.
    check_table = URL_DB.query.filter_by(short_url = f"https://makemeshort.com/{endpoint}").first()
    if check_table:
        # incrementing on every visits.
        check_table.visits += 1
        db.session.commit()
        return redirect(check_table.long_url)
    else:
        abort(404)

@views.route('/api', methods = ["GET", "POST"])
def api_home():
    if request.method == "GET":
        json_data = {
                        "success" : False,
                        "message" : "use post method to short an url"
                    }
        return jsonify(json_data)
    elif request.method == "POST":
        long_url = request.json["long_url"]
        custom_name = ""
        try:
            custom_name = request.json["custom_name"]
        except Exception:
            custom_name_name = None
        
        if not re.search(REGEX, long_url):
            json_data = {
                            "success" : False,
                            "message" : "invalid url"
                        }
            return jsonify(json_data)
        else:
            if not custom_name:
                custom_name = "".join(random.choices(string.ascii_lowercase + string.digits, k = 6))

            check_long_url = URL_DB.query.filter_by(long_url = long_url).first()
            if check_long_url:
                json_data = {
                                "success" : True,
                                "data" : {
                                    "long_url" : check_long_url.long_url,
                                    "short_url" : check_long_url.short_url,
                                    "date_time" : check_long_url.date,
                                    "visits" : check_long_url.visits
                                         }
                            }
                return jsonify(json_data)
            
            if custom_name:
                check_custom_name = URL_DB.query.filter_by(short_url = f"https://makemeshort.com/{custom_name}").first()
                if check_custom_name:
                    json_data = {
                                    "success" : False,
                                    "message" : "custom name already exists"
                                }
                    return jsonify(json_data)
            
            short_url = f"https://makemeshort.com/{custom_name}"
            put_db = URL_DB(long_url = long_url, short_url = short_url, visits = 0, ip_address = request.remote_addr)
            db.session.add(put_db)
            db.session.commit()

            json_data = {
                            "success" : True,
                            "data" : {
                                "long_url" : long_url,
                                "short_url" : short_url
                                     }
                        }
            return jsonify(json_data)

@views.route('/api/info')
def endpoint_info():
    if request.method == "GET":
        endpoint = request.args.get("endpoint")
        if not endpoint:
            json_data = {
                            "message" : "parameter missing",
                            "success" : False
                        }
            return jsonify(json_data)
        check_endpoint = URL_DB.query.filter_by(short_url = f"https://makemeshort.com/{endpoint}").first()
        if not check_endpoint:
            json_data = {
                            "message" : "such endpoint does not exist",
                            "success" : False
                        }
        else:
            json_data = {
                            "success" : True,
                            "data" : {
                                        "long_url" : check_endpoint.long_url,
                                        "short_url" : check_endpoint.short_url,
                                        "date_time" : check_endpoint.date,
                                        "visits" : check_endpoint.visits,
                                        "ip_address" : check_endpoint.ip_address
                                     }
                        }
        return jsonify(json_data)
