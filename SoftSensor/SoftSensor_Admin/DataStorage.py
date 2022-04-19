from abc import ABC, abstractmethod

class DataStorage(ABC):
    """An interface for how to implement a data storage.

    Attributes
    ----------
    myDataReceiver : DataReceiver
        object to be notified whenever new data is received

    Methods
    -------
    notifyDataUpdate() : void
        notifies data receiver that there is new data
    setUp() : bool
        a method to handle the setUp of a data storage
    getData() : lst(double)
        get the inputs as defined in the setUp method
    receiveResults(results) : bool
        store the results as defined in the setUp method
    """

    def __init__(self, myDataReceiver):
        """DataStorage constructor.

        Parameters
        ----------
        myDataReceiver : DataReceiver
            object to be notified whenever new data is received

        Returns
        -------
            Nothing
        """
        self.myDataReceiver = myDataReceiver
        return

    @abstractmethod
    def notifyDataUpdate(self):
        """Notifies data receiver that there is new data 

        Parameters
        ----------
            Nothing

        Returns
        -------
            Nothing
        """
        pass

    @abstractmethod
    def checkExistanceOfNewData(self):
        """Checks whether there is new data

        Parameters
        ----------
            Nothing

        Returns
        -------
            True if there is new data, False otherwise
        """
        pass

    @abstractmethod
    def setUp(self):
        """A method to handle the setUp of a data storage.

        This method communicates with the user to establish how the 
        communication of with the data storage will happen as well as how
        the inputs and results will look like.

        Parameters
        ----------
            Nothing    

        Returns
        -------
        bool
            true if set up was successful, false otherwise
        """
        pass

    @abstractmethod
    def getData(self):
        """Get the inputs as defined in the setUp method

        Parameters
        ----------
            Nothing

        Returns
        -------
        inputs : lst(double)
            a list of doubles with each entry representing a numerical input
        """
        pass

    @abstractmethod
    def receiveResults(self, results):
        """Store the results as defined in the setUp method

        Parameters
        ----------
        results : lst(double)
            a list of doubles with each entry representing a numerical result

        Returns
        -------
        bool
            true if storage of results was successful, false otherwise
        """
        pass