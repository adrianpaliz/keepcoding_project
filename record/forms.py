from record import app
from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime

currencies_names = app.config["CURRENCIES"]


class PurchaseForm(FlaskForm):
    day = datetime.now().date()

    hour = datetime.now().time().isoformat()[:-3]

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
    amount_to = FloatField("Amount to buy")
    unit_price = FloatField("Unit price")
    calculate = SubmitField("Calculate")
    submit = SubmitField("Submit")
