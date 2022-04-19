from SoftSensor.SoftSensor_Admin import SoftSensor
from SoftSensor.SoftSensor_Admin import SoftSensorManager
import random
from tkinter import StringVar, Tk, Label, Entry, Button, OptionMenu

#import data storages
from SoftSensor.DataStorageImplementations import MQTTDataStorage, SQLDataStorage

#import estimators
from SoftSensor.EstimatorImplementations import ValvePressureDropEstimator
from SoftSensor.EstimatorImplementations import CtoFEstimator

#import ml models
from SoftSensor.MLModelImplementations import LSTMModel

class SoftSensorFactory():
    """A class used to create soft sensors.

    Attributes
    ----------
        Nothing

    Methods
    -------
    createPumpExampleSoftSensor() : mySoftSensor
        creates a SoftSensor for the pump example
    """

    @staticmethod
    def createSoftSensor(myManager, myDataStorage=None, myEstimator=None, myMLModel=None):
        print("************************ Factory creating soft sensor **************************")
        myDataStorage = [myDataStorage]
        myEstimator = [myEstimator]
        myMLModel = [myMLModel]
        tkWindow = Tk()
        tkWindow.title('Select Software Settings')
        tkWindow.eval('tk::PlaceWindow . center')
        options1 = StringVar()
        options1.set("Click Here")
        options2 = StringVar()
        options2.set("Click Here")
        options3 = StringVar()
        options3.set("Click Here")

        def createMe(myManager, myDataStorage, myEstimator, myMLModel):
            print("Creating soft sensor of type: ")
            print(options1.get())
            print(options2.get())
            print(options3.get())
            if options1.get() == "MQTT":
                myDataStorage[0] = MQTTDataStorage.MQTTDataStorage(myManager)
            elif options1.get() == "SQL":
                myDataStorage[0] = SQLDataStorage.SQLDataStorage(myManager)

            if options2.get() == "Valve Pressure Drop Estimator":
                myEstimator[0] = ValvePressureDropEstimator.ValvePressureDropEstimator()
            elif options2.get() == "C to F Estimator":
                myEstimator[0] = CtoFEstimator.CtoFEstimator()

            if options3.get() == "LSTM":
                myMLModel[0] = LSTMModel.LSTMModel()

            return True

        l1 = Label(tkWindow, text="Data Storage Type").grid(row=0, column=0)
        om1 = OptionMenu(tkWindow, options1, "MQTT", "SQL").grid(row=0, column=1)
        l2 = Label(tkWindow, text="Estimator Type").grid(row=1, column=0)
        om2 = OptionMenu(tkWindow, options2, "Valve Pressure Drop Estimator", "C to F Estimator").grid(row=1, column=1)
        l3 = Label(tkWindow, text="ML Model Type").grid(row=2, column=0)
        om3 = OptionMenu(tkWindow, options3, "LSTM", "No Model").grid(row=2, column=1)

        b = Button(tkWindow, text="OK", command=lambda: createMe(myManager, myDataStorage, myEstimator, myMLModel)).grid(row=3, column=0)
        # b.grid(pady=20, padx=40)
        quitButton = Button(tkWindow, text="Exit", command=tkWindow.destroy).grid(row=3, column=1)
        # quitButton.grid(pady=20, padx=80)
        tkWindow.mainloop()

        if myDataStorage[0] != None:
            myDataStorage[0].setUp()

        if myEstimator[0] != None:
            myEstimator[0].setUp()

        if myMLModel[0] != None:
            myMLModel[0].setUp()

        if (myDataStorage[0] != None and myEstimator[0] != None):
            mySoftSensor = SoftSensor.SoftSensor(myDataStorage[0], myEstimator[0], myMLModel[0], "No name")
            print("************************* Factory created soft sensor **************************")
            return mySoftSensor
        else:
            print("ERROR: Could not create soft sensor")
            return None

    @staticmethod
    def createSQLExampleSoftSensor(myManager):
        """Creates a SoftSensor for the SQL test

        Parameters
        ----------
            Nothing

        Returns
        -------
        mySoftSensor : SoftSensor
            newly created SoftSensor
        """

        print("******************** Factory creating SQL soft sensor demo *********************")
        my_sql_data_storage = SQLDataStorage.SQLDataStorage(myManager)
        my_sql_data_storage.setUp()
        myEstimator = ValvePressureDropEstimator.ValvePressureDropEstimator()
        myEstimator.setUp()
        myMLModel = None
        mySoftSensor = SoftSensor.SoftSensor(my_sql_data_storage, myEstimator, myMLModel, "SQL")
        print("******************** Factory created SQL soft sensor demo **********************")
        return mySoftSensor

    @staticmethod
    def createMQTTExampleSoftSensor(myManager):
        """Creates a SoftSensor for the MQTT test

        Parameters
        ----------
            Nothing

        Returns
        -------
        mySoftSensor : SoftSensor
            newly created SoftSensor
        """
        print("******************* Factory creating MQTT soft sensor demo *********************")
        my_mqtt_data_storage = MQTTDataStorage.MQTTDataStorage(myManager)
        # my_mqtt_data_storage.setUp()
        client = f"python-mqtt-{random.randint(0, 1000)}"
        broker = "broker.emqx.io"
        port = 1883
        user = "emqx"
        password = "public"
        input = "T_C"
        output = "T_F"
        my_mqtt_data_storage.validateLogin(client, broker, port, user, password, input, output)
        myEstimator = CtoFEstimator.CtoFEstimator()
        myMLModel = LSTMModel.LSTMModel()
        mySoftSensor = SoftSensor.SoftSensor(my_mqtt_data_storage, myEstimator, myMLModel, "MQTT")
        print("******************** Factory created MQTT soft sensor demo *********************")
        return mySoftSensor
