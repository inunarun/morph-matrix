"""
    :author: inunarun
             Aerospace Systems Design Laboratory,
             Georgia Institute of Technology,
             Atlanta, GA

    :date: 2018-04-15 15:19:05
"""

from typing import Optional, Any, Dict
from .matrixnode import MatrixNode
import numpy as np


class Component(MatrixNode):
    """

    """

    def __init__(self, name: str, parent: Optional[MatrixNode]=None, **kwargs):
        """

        :param name:
        :type name: str

        :param parent: default None,
        :type parent: MatrixNode

        :param kwargs:
        :type kwargs: dict
        """
        super().__init__(name, parent)
        self._properties = kwargs
        # self._incompatible_indices = []

    # def __getstate__(self) -> Dict:
    #     """

    #     :return:
    #     :rtype: dict
    #     """
    #     state = super().__getstate__()
    #     state.update({"properties": self._properties})
    #     return state

    # def __setstate__(self, state: Dict):
    #     """

    #     :param state:
    #     :type state: dict
    #     """
    #     super().__setstate__(state)
    #     self._properties = state.get("properties")

    # def to_json(self) -> Dict:
    #     """

    #     :return:
    #     :rtype: dict
    #     """
    #     json_state = super().to_json()
    #     json_state.update({"properties": self._properties})
    #     return json_state

    def index(self) -> int:
        """

        :return:
        :rtype: int
        """
        return self.get_system().options().index(self)

    def get_system(self) -> "System":
        """

        :return:
        :rtype: `morphologicalmatrix.system.System`
        """
        parent = self.parent()
        while parent.parent() is not None:
            parent = parent.parent()
        return parent

    def get_compatibilities(self) -> np.ndarray:
        """

        :return:
        :rtype: np.ndarray
        """
        system = self.get_system()
        compatibilities = system.compatibility_matrix()[:, self.index()]
        return compatibilities

    def get_property(self, property_name: str) -> Optional[Any]:
        """

        :param property_name:
        :type property_name: str

        :return:
        :rtype: Any
        """
        return self._properties.get(property_name)

    def alter_compatiblity(self, component: "Component", is_compatible: bool):
        """

        :param component:
        :type component: `morphologicalmatrix.component.Component`

        :param is_compatible:
        :type is_compatible: bool
        """
        value = 1 if is_compatible else 0
        matrix = self.get_system().compatibility_matrix()
        matrix[self.index(), component.index()] = value
