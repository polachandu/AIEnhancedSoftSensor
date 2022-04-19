class SoftSensor:
    """A class used to represent a soft sensor.

    Attributes
    ----------
    myDataStorage : DataStorage
        object used for getting input data and sending results
    myEstimator : Estimator
        object used for sending input data and getting results
    myMLModel : MLModel
        object used for training an ML model based on input data and results

    Methods
    -------
    runSoftSensor() : bool
        gets input from data storage and calculates results using estimator
    trainMLModel() : bool
        sends inputs and results to train MLModel
    """

    def __init__(self, myDataStorage, myEstimator, myMLModel=None, name = None):
        """SoftSensor constructor.

        Parameters
        ----------
        myDataStorage : DataStorage
            object used for getting input data and sending results
        myEstimator : Estimator
            object used for sending input data and getting results
        myMLModel : MLModel
            object used for training an ML model based on input data and results

        Returns
        -------
            Nothing
        """

        self.myDataStorage = myDataStorage
        self.myEstimator = myEstimator
        self.myMLModel = myMLModel
        self.name = name
        return

    def runSoftSensor(self):
        """Gets input from data storage and calculates results using estimator.

        After getting and sending results, the ML model is trained.

        Parameters
        ----------
            Nothing

        Returns
        -------
        bool
            true if operation was successful, false otherwise
        """
        message = " " + self.name + " Soft Sensor Running "
        num = int((80 - len(message))/2)
        if num < 3:
            num = 3
        for i in range(num):
            message = "-"+message+"-"
        if len(message) != 80:
            message += "-"
        print(message)
        # Get input data from data storage
        print("Getting new data")
        inputs = self.myDataStorage.getData()
        print("NEW DATA:")
        print(inputs)
        # Get results from estimator using inputs
        print("Estimating results")
        results = self.myEstimator.estimateResults(inputs)
        print("RESULTS:")
        print(results)
        # Send results for data storage
        print("Sending results to storage")
        retVal = self.myDataStorage.receiveResults(results)
        # train ML model
        print("Sending inputs and results to train ML model")
        self.trainMLModel(inputs, results)
        print("---------------------- Soft Sensor Successfully Finished -----------------------")

        return retVal

    def trainMLModel(self, inputs, results):
        """Sends inputs and results to train MLModel.

        Parameters
        ----------
            Nothing

        Returns
        -------
        metrics : lst(double)
            a list of all metrics
            :param results:
            :param inputs:
        """

        if self.myMLModel is not None:
            metrics = self.myMLModel.start_training(inputs, results)
        else:
            metrics = None

        return metrics
