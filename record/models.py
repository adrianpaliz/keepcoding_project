import sqlite3


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
                                    SELECT day, hour, currency_from, amount_from, currency_to, amount_to, id
                                    FROM movements
                                    ORDER BY day
                                """
        )

    def update_data(self, params):
        self.make_a_query(
            """
                            UPDATE movements set day = ?, hour = ?, currency_from = ?, amount_from = ?, currency_to = ?, amount_to = ? 
                            WHERE id = ?
                        """,
            (params),
        )
