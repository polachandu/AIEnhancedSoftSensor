import mysql.connector as connection
import pandas as pd

if __name__ == '__main__':

    def read_db():
        try:
            my_db = connection.connect(host="localhost", database='PUMPEXAMPLE', user="root", passwd="9788",
                                       use_pure=True)
            query = "SELECT * FROM PumpExample;"
            result = pd.read_sql(query, my_db)
            my_db.close()

        except Exception as e:
            my_db.close()
            print(str(e))

        print(result.head(5))


    def update_db(vector):
        mydb = connection.connect(
            host="localhost",
            user="root",
            password="9788",
            database="PUMPEXAMPLE"
        )
        my_cursor = mydb.cursor()
        query = "UPDATE PumpExample SET S_Pout_kPa = '2323' WHERE S_T_C = '20.000000' "
        my_cursor.execute(query)

        mydb.commit()


    read_db()
    update_db(23)
    read_db()
