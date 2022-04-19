from functools import partial
from tkinter import StringVar, Tk, Label, Entry, Button, OptionMenu
import mysql.connector
import pandas as pd

from SoftSensor.SoftSensor_Admin.DataStorage import DataStorage
from SoftSensor.DataStorageImplementations.SQLConnection import SQLConnection


class SQLDataStorage(DataStorage):

    def __init__(self, myDataReceiver=None):
        self.name = None
        self.password = None
        self.db_name = None
        self.connection = None
        self.column_name = []
        self.input_column=[]
        self.output_column=[]
        super().__init__(myDataReceiver)

    def setUp(self):
        # window
        tkWindow = Tk()
        tkWindow.title('Database Login Credentials')
        tkWindow.eval('tk::PlaceWindow . center')

        # database label and text entry box
        databaseLabel = Label(tkWindow, text="Database Name").grid(row=0, column=0)
        database = StringVar()
        databaseEntry = Entry(tkWindow, textvariable=database).grid(row=0, column=1)
        # username label and text entry box
        usernameLabel = Label(tkWindow, text="User Name").grid(row=1, column=0)
        username = StringVar()
        usernameEntry = Entry(tkWindow, textvariable=username).grid(row=1, column=1)

        # password label and password entry box
        passwordLabel = Label(tkWindow, text="Password").grid(row=2, column=0)
        password = StringVar()
        passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=2, column=1)

        validateLogin = partial(self.validateLogin, database, username, password)


        # login button
        loginButton = Button(tkWindow, text="Login", command=validateLogin)
        loginButton.grid(row=4, column=0)
        loginButton.grid(pady=20, padx=40)
        quitButton = Button(tkWindow, text="Exit", command=tkWindow.destroy)
        quitButton.grid(row=4, column=1)
        quitButton.grid(pady=20, padx=80)
        tkWindow.mainloop()
        return True

    def notifyDataUpdate(self):
        if self.checkExistanceOfNewData():
            self.myDataReceiver.notifyDataUpdate(self)

    def validateLogin(self, database, username, password):
        self.name = username.get()
        self.password = password.get()
        self.db_name = database.get()
        self.connection = SQLConnection(self.name, self.password, self.db_name)
        print("SQL Data Storage set up with following details:")
        print("username entered :", self.name)
        print("password entered :", self.password)
        print("database entered :", self.db_name)
        connection = self.connection.sql_connection()
        if connection[0] == "Success":
            db = connection[1]
            try:
                self.displayColumns()
            except:
                print("Failed to read database columns")
        else:
            print(connection[1])
        return

    def checkExistanceOfNewData(self):
        connection = self.connection.sql_connection()
        if connection[0] == "Success":
            db = connection[1]
            try:
                curs = db.cursor()
                # TODO: get rid of hard coded value, should use given output column names here
                curs.execute("select * from PE WHERE " + self.output_column[0] + " is null")
                records = curs.fetchall()
                return len(records) != 0
            except:
                print("Failed to read data from table")
            finally:
                if db:
                    db.close()
        else:
            print(connection[1])

        return False

    def getData(self):

        result_list = []
        connection = self.connection.sql_connection()
        if connection[0] == "Success":
            db = connection[1]
            try:
                result = pd.read_sql_query("SELECT " + ','.join(self.input_column) + " FROM PE WHERE " + ','.join(self.output_column) + " is null",db)
                result_list.append(result)
            except:
                print("Error")
            finally:
                if db:
                    db.close()
        else:
            print(connection[1])

        return result_list

    def receiveResults(self, results):

        retVal = [self.writeRow(out, id) for out, id in zip(results[0][self.output_column[0]], results[0]['ID'])]

        for x in retVal:
            if not x:
                return False
        return True

    def writeRow(self, out, id):
        connection = self.connection.sql_connection()
        if connection[0] == "Success":
            db = connection[1]
            try:
                curs = db.cursor()
                sql = "UPDATE PE SET " + self.output_column[0] + "= %s WHERE ID = %s"
                args = (str(out), str(id))
                curs.execute(sql, args)
                db.commit()
            except:
                print("Error writing results to database")
                if db:
                    db.rollback()
                return False
            finally:
                if db:
                    db.close()
        else:
            print(connection[1])
            return False
        return True

    def displayColumns(self):
        tkWindow = Tk()
        tkWindow.title('Select the columns')
        tkWindow.eval('tk::PlaceWindow . center')
        # try:
        db = mysql.connector.connect(host='localhost',
                                     user=self.name,
                                     password=self.password,
                                     db=self.db_name)
        curs = db.cursor()
        curs.execute("SHOW COLUMNS FROM PE")
        column_names = curs.fetchall()
        column_name = [(x[0]) for x in column_names]
        self.column_name = column_name.copy()

        def show(self):
            self.input_column = []
            self.output_column = []
            for i in range(len(column_names)):
                clicked_label = Label(tkWindow, text=clicked[i].get()).grid(row=i, column=3)
                if clicked[i].get() == "input":
                    self.input_column.append(column_name[i])
                if clicked[i].get() == "output":
                    self.output_column.append(column_name[i])
            i = i + 1
            print("input columns: ", self.input_column)
            print("output columns: ", self.output_column)
            return True

        clicked = []
        for i in range(len(column_names)):
            clicked.append(StringVar(tkWindow))
            clicked[i].set("input")
            options = ["input", "output"]
            column_label = Label(tkWindow, text=str(column_name[i]))
            column_label.grid(row=i, column=0)
            om = OptionMenu(tkWindow, clicked[i],*options)
            om.grid(row=i, column=1)
        i=i+1

        b = Button(tkWindow, text="OK", command=lambda: show(self))
        b.grid(row=i+1, column=0)
        b.grid(pady=20, padx=40)
        quitButton = Button(tkWindow, text="Exit", command=tkWindow.destroy)
        quitButton.grid(row=i + 1, column=1)
        quitButton.grid(pady=20, padx=80)
        tkWindow.mainloop()
        return True

