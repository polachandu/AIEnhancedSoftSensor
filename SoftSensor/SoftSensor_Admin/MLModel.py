from abc import ABC, abstractmethod


class MLModel(ABC):
    """An interface for how to implement an MLModel.

    Attributes
    ----------

    Methods
    -------
    trainModel(inputs, results) : lst(double)
        a method that trains the current model
    """

    @abstractmethod
    def train_model(self, inputs, results):
        """Trains the current model with given inputs and results.

        Uses the current model and trains it with the given inputs and results.
        Returns true if successfull training.

        Parameters
        ----------
        inputs : lst(double)
            a list of doubles with each entry representing a numerical input
        results : lst(double)
            a list of doubles with each entry representing a numerical result

        Returns
        -------
        metrics : lst(double)
            metrics of the model after training
        """
        pass

    def setup(self):
        """A method to handle the setUp of an ML model.

        This method communicates with the user to establish how the inputs
        will look like as well as how the results will look like.

        Parameters
        ----------
            Nothing

        Returns
        -------
        bool
            true if set up was successful, false otherwise
        """
        pass