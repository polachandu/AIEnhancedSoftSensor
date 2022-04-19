import time

from SoftSensor.SoftSensor_Admin.DataReceiver import DataReceiver
from SoftSensor.SoftSensor_Admin import SoftSensor
from SoftSensor.SoftSensor_Admin.SoftSensorFactory import SoftSensorFactory


class SoftSensorManager(DataReceiver):
    """A singleton manager to handle the operation of all soft sensors.

    Attributes
    ----------
    mySoftSensors : lst(SoftSensor)
        a list of all soft sensors

    Methods
    -------
    notifyDataUpdate(myUpdatedDataStorage) : void
        runs all soft sensors that use myUpdatedDataStorage
    addSoftSensor(newSoftSensor) : void
        adds newSoftSensor to the list of mySoftSensors
    """

    def __new__(cls):
        """Implementation of the singleton pattern.
        
        Parameters
        ----------
            Nothing  

        Returns
        -------
            Nothing
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(SoftSensorManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, ):
        """SoftSensorManager constructor.

        Parameters
        ----------
            Nothing

        Returns
        -------
            Nothing
        """
        self.mySoftSensors = []
        self.myDataStorages = []
        return

    def notifyDataUpdate(self, myUpdatedDataStorage):
        """Runs all soft sensors that use myUpdatedDataStorage

        Parameters
        ----------
        myUpdatedDataStorage : DataStorage
            a DataStorage object that has new inputs available

        Returns
        -------
            Nothing
        """
        print("######################### Manager notified of new data #########################")
        for sensor in self.mySoftSensors:
            if sensor.myDataStorage == myUpdatedDataStorage:
                sensor.runSoftSensor()
        print("############## Manager ran all soft sensors dependant on new data ##############\n")
        return

    def run(self):
        """Checks data storages for new data and runs soft sensors accordingly

        Returns
        -------
            Nothing
        """
        while True:
            for dataStorage in self.myDataStorages:
                if dataStorage.checkExistanceOfNewData():
                    self.notifyDataUpdate(dataStorage)
            time.sleep(0.1)
        return

    def createSoftSensor(self, type=None, myDataStorage=None, myEstimator=None, myMLModel=None):
        """Creates a SoftSensor based on its type

        Parameters
        ----------
        type : string
            type of soft sensor to be created

        Returns
        -------
        mySoftSensor : SoftSensor
            newly created SoftSensor
        """
        print("###################### Manager requesting new soft sensor ######################")
        mySoftSensor = None

        if type == None:
            mySoftSensor = SoftSensorFactory.createSoftSensor(self, myDataStorage, myEstimator, myMLModel)
        elif type == "SQLExample":
            mySoftSensor = SoftSensorFactory.createSQLExampleSoftSensor(self)
        elif type == "MQTTExample":
            mySoftSensor = SoftSensorFactory.createMQTTExampleSoftSensor(self)
        else:
            print("ERROR: Soft sensor of type ", type, " is not supported")

        self.addSoftSensor(mySoftSensor)
        print("######################## Manager added new soft sensor #########################\n")

        return mySoftSensor

    def addSoftSensor(self, newSoftSensor):
        """Adds newSoftSensor to the list of mySoftSensors

        Parameters
        ----------
        newSoftSensor : SoftSensor
            a SoftSensor object to be added to the list

        Returns
        -------
            Nothing
        """
        if (newSoftSensor != None):
            self.mySoftSensors.append(newSoftSensor)
            newDataStorage = True
            for dataStorage in self.myDataStorages:
                if newSoftSensor.myDataStorage == dataStorage:
                    newDataStorage = False
            if newDataStorage:
                self.myDataStorages.append(newSoftSensor.myDataStorage)
        return
