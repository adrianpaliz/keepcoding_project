from record import app
from flask_wtf import FlaskForm
from wtforms import DateField, TimeField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime

currencies_names = app.config["CURRENCIES"]


class PurchaseForm(FlaskForm):
    day = DateField(
        label=None, validators=None, format="%d-%m-%Y", default=datetime.now
    )
    hour = TimeField(
        label=None, validators=None, format="%H:%M:%S", default=datetime.now
    )
    currency_from = SelectField(
        "Currency form", validators=[DataRequired()], choices=currencies_names
    )
    currency_to = SelectField(
        "Currency to", validators=[DataRequired()], choices=currencies_names
    )
    amount_from = FloatField(
        "Amount to invest",
        validators=[DataRequired(), NumberRange(message="Must be a positive", min=1)],
    )
    # Remplace with api call
    amount_to = 34
    # Remplace with math operation
    unit_price = 1030
    submit = SubmitField("Submit")
