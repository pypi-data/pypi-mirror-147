""" TryCrime aigens Package """
import os
from .blog import Blog


__all__ = ['generators']


class AIGenerators:
    """ AIGenerators class"""
    def __init__(self):
        """ AIGenerators.__init__

        Initializes an AIGenerators object. Gets api_key from OS
        environment variable RAPID_API_KEY.

        Arguments:
            None

        Returns:
            Initialzed AIGenerators object.
        """

        self._api_key = os.getenv('RAPID_API_KEY')
        self.blog = Blog(self._api_key)


generators = AIGenerators()
