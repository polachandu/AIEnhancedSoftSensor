import mysql.connector


def getAllRows():
    try:
        connection = mysql.connector.connect(host="localhost",user="root",password="1234",database="pumpexample")
        cursor = connection.cursor()
        print("Connected to SQLite")

        select_query = "select * from pumpexample"
        cursor.execute(select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        for row in records:
            print("STC: ", row[0])
            print("S_Pin_kPa: ", row[1])
            print("S_F_kgh: ", row[2])
            print("S_E_kW: ", row[3])
            print("S_Pout_kPa: ", row[4])
            print("\n")

        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to read data from table", error)
    finally:
        if connection:
            connection.close()
            print("The Sqlite connection is closed")

# getAllRows()


# ------------------------------------------------------------------------------------------------

def getCommand(colName):
    switch={
        'STC': "select S_T_C from pumpexample",
        'PIN': "select v from pumpexample",
        'KGH': "select S_F_kgh from pumpexample",
        'KW': "select S_E_kW from pumpexample",
        'KKPAW': "select S_Pout_kPa from pumpexample",
    }
    return switch.get(colName,"Invalid input")


def getColumnName(colName):
    switch={
        'STC':"STC: ",
        'PIN': "S_Pin_kPa: ",
        'KGH': "S_F_kgh: ",
        'KW': "S_E_kW: ",
        'KKPAW': "S_Pout_kPa: ",
    }
    return switch.get(colName,"Invalid input")

def getSpecificColumn(colName):
    try:
        connection = mysql.connector.connect(host="localhost",user="root",password="1234",database="pumpexample")
        cursor = connection.cursor()
        print("Connected to SQLite")
        # get the command
        select_query=   getCommand(colName)
        # get the column name to show in result
        column_name=getColumnName(colName)

        cursor.execute(select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row\n")
        print(column_name,"\n")
        for row in records:
            print(row[0],"\n")

        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to read data from table", error)
    finally:
        if connection:
            connection.close()
            print("The Sqlite connection is closed")

getSpecificColumn("PIN")