from abc import ABC, abstractmethod


class DataReceiver(ABC):
    """An interface for how to implement an observer for data storage.

    Attributes
    ----------

    Methods
    -------
    notifyDataUpdate(myUpdatedDataStorage) : void
        method is called when myUpdatedDataStorage has new data
    """

    @abstractmethod
    def notifyDataUpdate(self, myUpdatedDataStorage):
        """Method is called when myUpdatedDataStorage has new data

        Parameters
        ----------
        myUpdatedDataStorage : DataStorage
            a DataStorage object that has new inputs available

        Returns
        -------
            Nothing
        """
        pass
