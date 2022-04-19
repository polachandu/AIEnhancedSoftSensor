import time
from datetime import datetime
from random import random

import pandas as pd
from IPython.display import display
import mysql.connector


class DataGenerator:
    def __init__(self, name, password, db_name):
        self.name = name
        self.password = password
        self.db_name = db_name

    def generate_random_data(self):
        db = mysql.connector.connect(host='localhost',
                                     user=self.name,
                                     password=self.password,
                                     db=self.db_name)

        while True:
            try:
                curs = db.cursor()
                args = [20.0 + 2.0 * random(), 100.0 + 10.0 * random(), 10.0 + random(), random(), datetime.date(datetime.now()), datetime.time(datetime.now())]
                curs.callproc('InsertPE', args)
                display(pd.read_sql_query('SELECT * FROM PE order by ID desc limit 1', db))
                db.commit()
                print("Data committed")
                time.sleep(3)

            except:
                print("Error")
                db.rollback()

        return


if __name__ == "__main__":
    my_generator = DataGenerator("root", "1234", "pe")
    my_generator.generate_random_data()
