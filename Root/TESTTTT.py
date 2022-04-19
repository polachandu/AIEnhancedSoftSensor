import time

import mysql.connector
import pandas as pd
from IPython.core.display import display


class DataGenerator:
    def __init__(self, name, password, db_name):
        self.name = name
        self.password = password
        self.db_name = db_name

    def generate_random_data(self):


        while True:
            db = mysql.connector.connect(host='localhost',
                                         user=self.name,
                                         password=self.password,
                                         db=self.db_name)
            display(pd.read_sql_query('SELECT * FROM PE order by ID desc limit 3', db))
            db.close()
            time.sleep(3)


if __name__ == "__main__":
    my_generator = DataGenerator("root", "9788", "pe")
    my_generator.generate_random_data()
