
import flask
from flask import request,json,jsonify
import mysql.connector


app=flask.Flask(__name__)


app.config["Debug"]=True


# get all the data 
@app.route("/home",methods=["Get"])
def getAllData():
    connection = mysql.connector.connect(host="localhost",user="root",password="1234",database="pumpexample")
    cursor = connection.cursor()
    select_query = "select * from pumpexample"
    cursor.execute(select_query)
    records = cursor.fetchall()
    print("Total rows are:  ", len(records))
    print("Printing each row")
    resultRow="STC,S_Pin_kPa,S_F_kgh,S_E_kW,S_Pout_kPa\n"
    for row in records:
            resultRow=resultRow+str(row[0])+','+ str(row[1])+','+str(row[2])+','+ str(row[3])+','+ str(row[4])+'\n'
    return resultRow


# get STC column the data 
@app.route("/STC",methods=["Get"])
def getSTCColumn():
    connection = mysql.connector.connect(host="localhost",user="root",password="1234",database="pumpexample")
    cursor = connection.cursor()
    select_query = "select S_T_C from pumpexample"
    cursor.execute(select_query)
    records = cursor.fetchall()
    print("Total rows are:  ", len(records))
    print("Printing each row")
    resultRow="S_T_C\n"
    for row in records:
            resultRow=resultRow+str(row[0])+'\n'
    return resultRow

# get KGH column the data 
@app.route("/KGH",methods=["Get"])
def getKGHColumn():
    connection = mysql.connector.connect(host="localhost",user="root",password="1234",database="pumpexample")
    cursor = connection.cursor()
    select_query = "select S_F_kgh from pumpexample"
    cursor.execute(select_query)
    records = cursor.fetchall()
    print("Total rows are:  ", len(records))
    print("Printing each row")
    resultRow="S_F_kgh\n"
    for row in records:
            resultRow=resultRow+str(row[0])+'\n'
    return resultRow

# get PIN column the data 
@app.route("/PIN",methods=["Get"])
def getPINColumn():
    connection = mysql.connector.connect(host="localhost",user="root",password="1234",database="pumpexample")
    cursor = connection.cursor()
    select_query = "select S_Pin_kPa from pumpexample"
    cursor.execute(select_query)
    records = cursor.fetchall()
    print("Total rows are:  ", len(records))
    print("Printing each row")
    resultRow="S_Pin_kPa\n"
    for row in records:
            resultRow=resultRow+str(row[0])+'\n'
    return resultRow    

# get KW column the data 
@app.route("/KW",methods=["Get"])
def getKWColumn():
    connection = mysql.connector.connect(host="localhost",user="root",password="1234",database="pumpexample")
    cursor = connection.cursor()
    select_query = "select S_E_kW from pumpexample"
    cursor.execute(select_query)
    records = cursor.fetchall()
    print("Total rows are:  ", len(records))
    print("Printing each row")
    resultRow="S_E_kW\n"
    for row in records:
            resultRow=resultRow+str(row[0])+'\n'
    return resultRow    


@app.route("/KKPAW",methods=["Get"])
def getKKPAWColumn():
    connection = mysql.connector.connect(host="localhost",user="root",password="1234",database="pumpexample")
    cursor = connection.cursor()
    select_query = "select S_Pout_kPa from pumpexample"
    cursor.execute(select_query)
    records = cursor.fetchall()
    print("Total rows are:  ", len(records))
    print("Printing each row")
    resultRow="S_Pout_kPa\n"
    for row in records:
            resultRow=resultRow+str(row[0])+'\n'
    return resultRow            

if __name__=="__main__":
    app.run()