"""
    :author: inunarun
             Aerospace Systems Design Laboratory,
             Georgia Institute of Technology,
             Atlanta, GA

    :date: 2018-04-15 15:17:25
"""

from .component import Component
from .system import System
from typing import Dict
import pickle as pk
import json


class MorphologicalMatrix(object):
    """

    """

    def __init__(self, system_name: str):
        """

        .. todo::

            Enable multiple systems so that we can have multiple different
            morphological matrices

        :param system_name:
        :type system_name: str
        """
        super().__init__()
        self._root = System(system_name)

    # def __getstate__(self) -> Dict:
    #     """

    #     :return:
    #     :rtype: dict
    #     """
    #     return {
    #         "system": self._root
    #     }

    # def __setstate__(self, state: Dict):
    #     """

    #     :param state:
    #     :type state: dict
    #     """
    #     self._root = state.get("system")

    def __getitem__(self, index: int) -> Component:
        """

        :return index:
        :type index: int

        :return:
        :rtype: `morphologicalmatrix.component.Component`
        """
        return self.system().options()[index]

    def system(self) -> System:
        """

        :return:
        :rtyoe: `morphologicalmatrix.system.System`
        """
        return self._root

    # def to_json(self) -> Dict:
    #     """

    #     :return:
    #     :rtype: dict
    #     """
    #     return {
    #         "system": self.system().to_json(),
    #     }

    def save(self, filename: str):
        """

        :param filename:
        :type filename: str
        """
        # with open(filename.replace("pk", "json"), "w") as fout:
        #     json.dump(self.to_json(), fout, indent=4)

        with open(filename, 'wb') as fout:
            pk.dump(self, fout)

    # @classmethod
    # def from_json(self, content: Dict):
    #     """

    #     :param content:
    #     :type content: dict
    #     """
    #     system_content = content.get("system")
    #     system = System.from_json(system_content)
    #     self._root = system

    @classmethod
    def load(self, filename: str) -> "MorphologicalMatrix":
        """

        :param filename:
        :type filename: str

        :return:
        :rtype: `morphologicalmatrix.morphologicalmatrix.MorphologicalMatrix`
        """
        with open(filename, "rb") as fin:
            loaded_object = pk.load(fin)
        return loaded_object
