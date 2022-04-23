from flask import redirect, render_template, request, url_for
from record import app
from record.models import ProcessData
from record.forms import PurchaseForm
from record.models import APIRequest
import sqlite3

database_path = app.config["DATABASE_PATH"]
data_manager = ProcessData(database_path)


@app.route("/")
def home():
    data = data_manager.recover_data()
    return render_template("transactions.html", movements=data, navbar="Home")


@app.route("/buy", methods=["GET", "POST"])
def buy():
    instantiated_form = PurchaseForm()

    if request.method == "GET":
        return render_template("buy.html", jinja_form=instantiated_form, navbar="Buy")

    elif request.method == "POST":

        if instantiated_form.calculate.data == True:
            currency_from = request.form["currency_from"]
            currency_to = request.form["currency_to"]
            day = request.form["day"]

            hour = request.form["hour"]

            str_rate_time = day + "T" + hour

            form_api_request = APIRequest(currency_from, currency_to, str_rate_time)
            rate = form_api_request.get_rate()
            instantiated_form = PurchaseForm()
            instantiated_form.unit_price.data = rate

            amount_to_invest = instantiated_form.amount_from.data
            instantiated_form.amount_to.data = rate * amount_to_invest

            return render_template(
                "buy.html", jinja_form=instantiated_form, navbar="Buy"
            )

        elif instantiated_form.submit.data == True:

            params = (
                str(instantiated_form.day.strftime("%d/%m/%Y")),
                str(instantiated_form.hour),
                str(instantiated_form.currency_from.data),
                str(instantiated_form.currency_to.data),
                str(instantiated_form.amount_from.data),
                str(instantiated_form.amount_to.data),
                str(instantiated_form.unit_price.data),
            )
            data_manager.update_data(params)
            return redirect(url_for("home"))

    else:
        raise Exception("Request method unknown")


@app.route("/status")
def status():

    con = sqlite3.connect()
    cur = con.cursor()

    con.close()

    return render_template("status.html", navbar="Status")
