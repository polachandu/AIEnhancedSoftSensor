from abc import ABC, abstractmethod


class Estimator(ABC):
    """An interface for how to implement an estimator.

    Attributes
    ----------
        Nothing

    Methods
    -------
    setUp() : bool
        a method to handle the setUp of an estimator
    estimateResults(inputs) : lst(double)
        run calculations with the given inputs to return results
    """

    @abstractmethod
    def setUp(self):
        """A method to handle the setUp of an estimator.

        This method communicates with the user to establish how the inputs
        for the estimateResults method will look like as well as how the
        results will look like.

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
    def estimateResults(self, inputs):
        """Run calculations with the given inputs to return results.

        Structure of inputs and results was previously defined in setUp.

        Parameters
        ----------
        inputs : lst(double)
            a list of doubles with each entry representing a numerical input

        Returns
        -------
        results : lst(double)
            a list of doubles with each entry representing a numerical result
        """
        pass
