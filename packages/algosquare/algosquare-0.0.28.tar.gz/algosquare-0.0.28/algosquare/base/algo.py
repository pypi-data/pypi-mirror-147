"""Algo base class to interface with AlgoSquare."""

from abc import ABC, abstractmethod

class Algo(ABC):
    """Base class for all algos."""
    @classmethod
    @abstractmethod
    def load(cls, filename):
        """
        Loads a model.

        Args:
            filename: string.

        Returns:
            A model that can be used for predictions.

        Raises:
            NotImplementedError: no implementation found in derived class.
        """
        raise NotImplementedError

    @abstractmethod
    def save(self, filename):
        """
        Saves model to file.

        Args:
            filename: string.

        Returns:
            None.

        Raises:
            NotImplementedError: no implementation found in derived class.
        """
        raise NotImplementedError

