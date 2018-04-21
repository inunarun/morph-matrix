"""
    :author: inunarun
             Aerospace Systems Design Laboratory,
             Georgia Institute of Technology,
             Atlanta, GA

    :date: 2018-04-15 15:19:10
"""

from .matrixnodecollection import MatrixNodeCollection
from typing import Union, List, Optional, Dict
from .component import Component


class SubSystem(MatrixNodeCollection):
    """

    """

    def __init__(self, name: str, parent: Optional["MatrixNode"]=None,
                 allows_inter_compatibility: Optional[bool]=False):
        """

        :param name:
        :type name: str

        :param parent: default None,
        :type parent: `morphologicalmatrix.matrixnode.MatrixNode`

        :param allows_inter_compatibility: default False,
        :type allows_inter_compatibility: bool
        """
        super().__init__(name, parent)
        self._allows_inter_compatibility = allows_inter_compatibility

    # def __getstate__(self) -> Dict:
    #     """

    #     :return:
    #     :rtype: dict
    #     """
    #     state = super().__getstate__()
    #     state.update({
    #         "allows_inter_compatibility": self.allows_inter_compatibility()
    #     })
    #     return state

    # def __setstate__(self, state: Dict):
    #     """

    #     :param state:
    #     :type state: dict
    #     """
    #     super().__setstate__(state)
    #     self._allows_inter_compatibility = state.get("allows_inter_compatibility")

    # @staticmethod
    # def type() -> str:
    #     """

    #     :return:
    #     :rtype: str
    #     """
    #     return "subsystem"

    # def to_json(self) -> Dict:
    #     """

    #     :return:
    #     :rtype: dict
    #     """
    #     json_state = super().to_json()
    #     allows_inter_compat = self.allows_inter_compatibility()
    #     json_state.update({
    #         "allows_inter_compatibility": bool(allows_inter_compat),
    #     })
    #     return json_state

    def allows_inter_compatibility(self) -> bool:
        """

        :return:
        :rtype: bool
        """
        return self._allows_inter_compatibility

    def get_system(self) -> "System":
        """

        :return:
        :rtype: `morphologicalmatrix.system.System`
        """
        parent = self.parent()
        while parent.parent() is not None:
            parent = parent.parent()
        return parent

    def add_subsystem(self, subsystem: Union["SubSystem", str],
                      allow_inter_compatibility: bool):
        """

        :param subsystem:
        :type subsystem: `morphologicalmatrix.subsystem.SubSystem`

        :param allow_inter_compatibility:
        :type allow_inter_compatibility: bool
        """
        if isinstance(subsystem, str):
            subsystem = SubSystem(subsystem, self, allow_inter_compatibility)
        self.append(subsystem)

    def add_component(self, component: Union[Component, str], **kwargs):
        """

        :param component:
        :type component: `morphologicalmatrix.component.Component`

        :param kwargs:
        :type kwargs: dict
        """
        if isinstance(component, str):
            component = Component(component, self, **kwargs)
        self.append(component)
        self.__update_compatibilities()

    def add_custom_child(self, *args, **kwargs):
        """

        """
        super().add_custom_child(*args, **kwargs)
        self.__update_compatibilities()

    def selected_components(self) -> List[Component]:
        """

        :return:
        :rtype: list of Component
        """
        selected = []
        for child in self:
            if isinstance(child, Component):
                if child.is_selected():
                    selected.append(child)
            else:
                selected.extend(child.selected_components())
        return selected

    def __update_compatibilities(self):
        """
        Private method:
        """
        system = self.get_system()
        matrix = system.compatibility_matrix()
        local_alts = self.options()
        count = len(local_alts)
        for i in range(count):
            for j in range(i, count):
                if i == j:
                    comp_val = 1
                else:
                    comp_val = 1 if self.allows_inter_compatibility() else 0
                matrix[local_alts[i].index(), local_alts[j].index()] = comp_val
