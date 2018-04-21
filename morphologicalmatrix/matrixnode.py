"""
    :author: inunarun
             Aerospace Systems Design Laboratory,
             Georgia Institute of Technology,
             Atlanta, GA

    :date: 2018-04-15 15:19:22
"""

from typing import Optional, Dict


class MatrixNode(object):
    """

    """

    def __init__(self, name: str, parent: Optional["MatrixNode"]=None):
        """

        :param name:
        :type name: str

        :param parent: default None,
        :type parent: `morphologicalmatrix.matrixnode.MatrixNode`
        """
        super().__init__()
        self._name = name
        self._parent = parent
        self._is_selected = False

    def __str__(self) -> str:
        """

        :return:
        :rtype: str
        """
        representation = super().__str__()
        return "{{{0} at {1}}}".format(representation, hex(id(self)))

    def __repr__(self) -> str:
        """

        :return:
        :rtype: str
        """
        return "{0}: {1}".format(self.get_name(), self.is_selected())
        # return "{0}: [{1}]".format(self.get_name(),
        #                            ", ".join([entity.get_name()
        #                                       for entity in self]))

    # def __getstate__(self) -> Dict:
    #     """

    #     :return:
    #     :rtype: dict
    #     """
    #     return {
    #         "name": self.get_name(),
    #         "is_selected": self.is_selected(),
    #         "parent": self.parent(),
    #     }

    # def __setstate__(self, state) -> Dict:
    #     """

    #     :param state:
    #     :type state: Dict
    #     """
    #     self._name = state.get("name")
    #     self._is_selected = state.get("is_selected")
    #     self._parent = state.get("parent")

    # def to_json(self) -> Dict:
    #     """

    #     :return:
    #     :rtype: dict
    #     """
    #     return {
    #         "name": self.get_name(),
    #         "is_selected": self.is_selected(),
    #         # "parent": self.parent().to_json(),
    #     }

    def parent(self) -> "MatrixNode":
        """

        :return:
        :rtype: `morphologicalmatrix.matrixnode.MatrixNode`
        """
        return self._parent

    def is_selected(self) -> bool:
        """

        :return:
        :rtype: bool
        """
        return self._is_selected

    def allows_selection(self) -> bool:
        """

        :return:
        :rtype: bool
        """
        return True

    def get_name(self) -> str:
        """

        :return:
        :rtype: str
        """
        return self._name

    def set_selected(self, is_selected: bool):
        """

        :param is_selected:
        :type is_selected: bool
        """
        if not self.allows_selection():
            raise TypeError("%s does not support selection." % self.get_name())
        self._is_selected = is_selected
