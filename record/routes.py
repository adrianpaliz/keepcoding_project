from flask import flash, redirect, render_template, request, url_for
from record import app
from record.models import ProcessData
from record.forms import PurchaseForm
from record.models import APIRequest
from datetime import datetime
import sqlite3, requests


database_path = app.config["DATABASE_PATH"]
cryptocurrencies = app.config["CRYPTOCURRENCIES"]


data_manager = ProcessData(database_path)


@app.route("/")
def home():
    try:
        data = data_manager.recover_data()
        return render_template("transactions.html", movements=data, navbar="Home")
    except sqlite3.Error as error:
        flash("Database error.")
        return render_template("transactions.html", movements=[], navbar="Home")


@app.route("/buy", methods=["GET", "POST"])
def buy():
    instantiated_form = PurchaseForm()

    if request.method == "POST":
                
        if instantiated_form.calculate.data == True:

            currency_from = request.form["currency_from"]
            currency_to = request.form["currency_to"]

            try:
                wallet = data_manager.get_wallet()
            except sqlite3.Error as error:
                flash("Database error")
                return redirect(url_for("buy"))

            if (
                instantiated_form.currency_from.data
                == instantiated_form.currency_to.data
            ):
                flash("You cannot buy one currency with the same currency.")
                return render_template(
                    "buy.html", jinja_form=instantiated_form, navbar="Buy"
                )

            elif (
                instantiated_form.currency_from.data in cryptocurrencies
                and instantiated_form.amount_from_hidden.data
                > wallet[instantiated_form.currency_from.data]
            ):
                flash(
                    "You don't have that amount of "
                    + instantiated_form.currency_from.data
                )
                return render_template(
                    "buy.html", jinja_form=instantiated_form, navbar="Buy"
                )

            else:
                day = request.form["day"]

                hour = request.form["hour"]

                str_rate_time = day + "T" + hour

                form_api_request = APIRequest(currency_from, currency_to, str_rate_time)
                response = form_api_request.query_rate()                

                try:
                    response.raise_for_status()
                except requests.RequestException as error:
                    if response.status_code == 400:
                        flash("There is something wrong with your request")
                    elif response.status_code == 401:
                        flash("Your API key is wrong")
                    elif response.status_code == 403:
                        flash("Your API key doesnt't have enough privileges to access this resource")
                    elif response.status_code == 429:
                        flash("You have exceeded your API key rate limits")
                    elif response.status_code == 550:
                        flash("You requested specific single item that we don't have at this moment")
                    else:
                        print("{}, Unknow error code".format(response.status_code))

                    return render_template(
                    "buy.html", jinja_form=instantiated_form, navbar="Buy"
                    )

                rate = form_api_request.get_rate()
                instantiated_form = PurchaseForm()
                instantiated_form.unit_price.data = rate

                amount_to_invest = instantiated_form.amount_from.data
                amount_from_invest_hidden = instantiated_form.amount_from.data
                                            
                instantiated_form.amount_to.data = rate * amount_to_invest
                instantiated_form.amount_from_hidden.data = request.form.getlist('amount_from_hidden')

                return render_template(
                    "buy.html", jinja_form=instantiated_form, navbar="Buy"
                )

        elif instantiated_form.submit.data == True:
            params = (
                str(instantiated_form.day.strftime("%d/%m/%Y")),
                str(instantiated_form.hour),
                str(instantiated_form.currency_from.data),
                str(instantiated_form.currency_to.data),
                str(instantiated_form.amount_from_hidden.data),
                str(instantiated_form.amount_to_hidden.data),
                str(instantiated_form.unit_price.data),
            )
            try:
                data_manager.update_data(params)
                return redirect(url_for("buy"))
            except sqlite3.Error as error:
                flash("Database error.")
                return render_template("buy.html", jinja_form=instantiated_form, navbar="Buy")

    else:
        return render_template("buy.html", jinja_form=instantiated_form, navbar="Buy")


@app.route("/status")
def status():

    wallet = data_manager.get_wallet()

    day = str(datetime.now().date())
    hour = datetime.now().time().isoformat()[:-3]
    str_rate_time = day + "T" + hour

    crypto_total_value_eur = 0
    for crypto in cryptocurrencies:
        form_api_request = APIRequest(crypto, "EUR", str_rate_time)
        rate = form_api_request.get_rate()
        crypto_total_value_eur += rate * wallet[crypto]

    return render_template(
        "status.html",
        navbar="Status",
        eur_investment=abs(wallet["EUR"]),
        crypto_value=crypto_total_value_eur,
    )
