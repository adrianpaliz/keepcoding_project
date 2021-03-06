import sqlite3, requests
from config import API_KEY, URL_SPECIFIC_RATE, CURRENCIES


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
            SELECT day, hour, currency_from, currency_to, amount_from_hidden, amount_to_hidden, unit_price
            FROM movements
            ORDER BY day
            """
        )

    def update_data(self, params):
        self.make_a_query(
            """
            INSERT INTO movements (day, hour, currency_from, currency_to, amount_from_hidden, amount_to_hidden, unit_price)
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
                wallet[row["currency_from"]] -= row["amount_from_hidden"]
            if row["currency_to"] in wallet:
                wallet[row["currency_to"]] += row["amount_to_hidden"]
        return wallet


class APIRequest:
    def __init__(self, currency_from="", currency_to="", rate_time=""):
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.rate_time = rate_time

    def query_rate(self):

        self.response =  requests.get(
            URL_SPECIFIC_RATE.format(
                self.currency_from, self.currency_to, self.rate_time, API_KEY
            ))
        return self.response

    def get_rate(self):
        return self.response.json()['rate']