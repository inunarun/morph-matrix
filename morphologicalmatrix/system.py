"""
    :author: inunarun
             Aerospace Systems Design Laboratory,
             Georgia Institute of Technology,
             Atlanta, GA

    :date: 2018-04-15 15:19:32
"""

from .matrixnodecollection import MatrixNodeCollection
from .compatibilitymatrix import CompatibilityMatrix
from .component import Component
from .subsystem import SubSystem
from typing import Union, Dict


class System(MatrixNodeCollection):
    """

    """

    def __init__(self, name: str):
        """

        :param name:
        :type name: str
        """
        super().__init__(name)
        self._compatibilities = CompatibilityMatrix(0)

    # def __getstate__(self) -> Dict:
    #     """

    #     :return:
    #     :rtype: dict
    #     """
    #     state = super().__getstate__()
    #     state.update({"compatibilities": self.compatibility_matrix()})
    #     return state

    # def __setstate__(self, state: Dict):
    #     """

    #     :param state:
    #     :type state:
    #     """
    #     super().__setstate__(state)
    #     self._compatibilities = state.get("compatibilities")

    # def to_json(self) -> Dict:
    #     """

    #     :return:
    #     :rtype: dict
    #     """
    #     json_state = super().to_json()
    #     json_state.update({
    #         "compatibilities": self.compatibility_matrix().to_json(),
    #     })
    #     return json_state

    def compatibility_matrix(self) -> CompatibilityMatrix:
        """

        :return:
        :rtype: `morphologicalmatrix.compatibilitymatrix.CompatibilityMatrix`
        """
        if self._compatibilities.shape[0] != self.options_count():
            compatibilities = CompatibilityMatrix(self.options_count())
            compatibilities.reinitialize_from(self._compatibilities)
            self._compatibilities = compatibilities
        return self._compatibilities

    def add_subsystem(self, subsystem: Union[SubSystem, str],
                      allow_inter_compatibility: bool=False):
        """

        :param subsystem:
        :type subsystem: str or `morphologicalmatrix.subsystem.SubSystem`

        :param allow_inter_compatibility: default False,
        :type allow_inter_compatibility: bool
        """
        if isinstance(subsystem, str):
            subsystem = SubSystem(subsystem, self, allow_inter_compatibility)
        self.append(subsystem)

    # @classmethod
    # def from_json(cls, content: Dict):
    #     """

    #     :param content:
    #     :type content: dict
    #     """
    #     created_object = super().from_json(content)
    #     saved_compats = content.get("compatibilities")
    #     created_object._compatibilities = Compatibilities.from_json(saved_compats)
    #     return created_object
