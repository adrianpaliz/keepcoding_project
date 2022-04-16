import sqlite3
from flask import render_template, flash, request
from record import app
from record.models import ProcessData
from record.forms import PurchaseForm
from record.models import APIRequest

database_path = app.config["DATABASE_PATH"]
data_manager = ProcessData(database_path)


@app.route("/")
def home():
    data = data_manager.recover_data()
    return render_template("transactions.html", movements=data)


@app.route("/buy", methods=["GET", "POST"])
def buy():
    instantiated_form = PurchaseForm()

    if request.method == "GET":
        return render_template("buy.html", jinja_form=instantiated_form)

    elif request.method == 'POST':
        currency_from = request.form['currency_from']
        currency_to = request.form['currency_to']
        day = request.form['day']
        hour = request.form['hour']        
        
        str_rate_time = day + "T" + hour
        rate_time = str_rate_time     

        form_api_request = APIRequest(currency_from, currency_to, rate_time)        
        rate = form_api_request.get_rate()   
                 
        instantiated_form = PurchaseForm()
        instantiated_form.unit_price = rate         

        return render_template("buy.html", jinja_form=instantiated_form)
    else:
        raise Exception("Request method unknown")


@app.route("/status")
def status():
    return render_template("status.html")
