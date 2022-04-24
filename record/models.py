import sqlite3, requests
from config import API_KEY, URL_SPECIFIC_RATE, CURRENCIES
from record.errors import APIError


class ProcessData:
    def __init__(self, file):
        self.database_source = file

    def create_dictionary(self, cur):
        rows = cur.fetchall()

        fields = []
        for item in cur.description:
            fields.append(item[0])

        result = []
        for row in rows:
            record = {}

            for key, value in zip(fields, row):
                record[key] = value
            result.append(record)
        return result

    def data_accessed(self, cur, con):
        if cur.description:
            datum_accessed = self.create_dictionary(cur)
        else:
            datum_accessed = None
            con.commit()
        return datum_accessed

    def make_a_query(self, query, params=[]):
        con = sqlite3.connect(self.database_source)
        cur = con.cursor()
        cur.execute(query, params)
        datum_accessed = self.data_accessed(cur, con)
        con.close()
        return datum_accessed

    def recover_data(self):
        return self.make_a_query(
            """
            SELECT day, hour, currency_from, currency_to, amount_from, amount_to, unit_price
            FROM movements
            ORDER BY day
            """
        )

    def update_data(self, params):
        self.make_a_query(
            """
            INSERT INTO movements (day, hour, currency_from, currency_to, amount_from, amount_to, unit_price)
                values(?, ?, ?, ?, ?, ?, ?) 
            """,
            params,
        )

    def recover_all_transaction(self):
        return self.make_a_query(
            """
            SELECT * FROM movements
            """
        )

    def get_wallet(self):
        wallet = {}
        for code in CURRENCIES:
            wallet[code] = 0

        data = self.recover_all_transaction()

        for row in data:
            if row["currency_from"] in wallet:
                wallet[row["currency_from"]] -= row["amount_from"]
            if row["currency_to"] in wallet:
                wallet[row["currency_to"]] += row["amount_to"]
        return wallet


class APIRequest:
    def __init__(self, currency_from="", currency_to="", rate_time=""):
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.rate_time = rate_time

    def get_rate(self):
        self.rate_request = requests.get(
            URL_SPECIFIC_RATE.format(
                self.currency_from, self.currency_to, self.rate_time, API_KEY
            )
        )
        if self.rate_request.status_code != 200:
           raise APIError(self.rate_request.json()["error"])
        return self.rate_request.json()["rate"]
