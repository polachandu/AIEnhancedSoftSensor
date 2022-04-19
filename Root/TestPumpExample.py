from datetime import datetime
import time
from random import random
from IPython.core.display import display
import mysql.connector
import pandas as pd
from SoftSensor.SoftSensor_Admin.SoftSensorManager import SoftSensorManager


def modelDataEntry(username, password, db_name):
    """
    Connects to database with given credentials then adds an entry
    """
    db = None
    try:
        db = mysql.connector.connect(host='localhost',
                                     user=username,
                                     password=password,
                                     db=db_name)

        myCursor = db.cursor()

        args = [random(), random(), random(), random(), datetime.date(datetime.now()),
                datetime.time(datetime.now())]

        myCursor.callproc('InsertPE', args)

        myCursor.execute("select * from PE ORDER BY ID DESC LIMIT 1")
        print("Entry added to database: ")
        print(myCursor.fetchone())

        db.commit()
    except:
        print("Error writing new row to database")
        if db:
            db.rollback()

    if db:
        db.close()


def displayDB(username, password, db_name):
    db = None
    try:
        db = mysql.connector.connect(host='localhost',
                                     user=username,
                                     password=password,
                                     db=db_name)

        curs = db.cursor()
        display(pd.read_sql_query('SELECT * FROM PE', db))
    except:
        print("Error connecting to database")

    if db:
        db.close()


if __name__ == "__main__":
    print("Test begun...")
    # 1. Create app
    print("Creating manager...")
    myManager = SoftSensorManager()
    print("... created manager")
    # 2. Create soft sensor
    print("Creating soft sensor...")
    myManager.createSoftSensor("PumpExample")
    print("... created soft sensor")
    # 3. Change SQL database
    print("Simulating data input to database...")
    for i in range(20):
        modelDataEntry("root", "9788", "PE")
        time.sleep(1)
        # You can test the workflow of running the soft sensor by uncommenting out this line
        # However, we need to figure out a way for this test to work without uncommenting out this line
        # Maybe some sort of multithreading in SQLDataStorage or SoftSensorManager that is constantly looking
        # if checkExistingOfNewData is true? We need to figure this out...
        # myManager.mySoftSensors[0].myDataStorage.notifyDataUpdate()
    print("... stop data input to database")
    # 4. Check if soft sensor worked
    time.sleep(10)
    print("Values in Pout column should be Pin + 50:")
    displayDB("root", "9788", "PE")
    print("...test ended")
