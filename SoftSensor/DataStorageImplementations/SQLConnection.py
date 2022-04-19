# added by behnaz for Sql Connection
import mysql.connector
from mysql.connector import errorcode


class SQLConnection:

    def __init__(self, name, password, db_name):
        self.name = name
        self.password = password
        self.db_name = db_name

    def sql_connection(self):
        status = ""
        message = ""
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 user=self.name,
                                                 password=self.password,
                                                 db=self.db_name)
            if connection.is_connected():
                db_Info = connection.get_server_info()
                # print("Connected to MySQL Server version ", db_Info)
                status = "Success"
                message = connection

        except mysql.connector.Error as err:
            status = "Fail"
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                message = "Something is wrong with your user name or password"
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                message = "Database does not exist"
                print("Database does not exist")
            else:
                print(err)
                message = "Error!"
        return status, message


# ------------------------------Test----------------------------------------
# if __name__ == "__main__":
#     sql = SQLConnection("root", "1234", "pe")
#     sql.sql_connection()
