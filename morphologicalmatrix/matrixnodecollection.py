"""
    :author: inunarun
             Aerospace Systems Design Laboratory,
             Georgia Institute of Technology,
             Atlanta, GA

    :date: 2018-04-15 15:54:40
"""

from typing import Union, Optional, Any, Callable, List, Dict
# from abc import ABCMeta, abstractmethod
from .matrixnode import MatrixNode
from functools import partial


class MatrixNodeCollection(MatrixNode, list):
    """

    """

    registry = {}

    def __init__(self, name: str, parent: Optional[MatrixNode]=None):
        """

        :param name:
        :type name: str

        :param parent: default None,
        :type parent: `morphologicalmatrix.matrixnode.MatrixNode` or
            `morphologicalmatrix.matrixnodecollection.MatrixNodeCollection`
        """
        MatrixNode.__init__(self, name, parent)
        list.__init__([])

    def __repr__(self) -> str:
        """

        :return:
        :rtype: str
        """
        return "{0}: [{1}]".format(self.get_name(),
                                   ", ".join([entity.get_name()
                                              for entity in self]))

        # representation = super().__repr__()
        # return "{0} [{1}]: {2}".format(self.get_name(),
        #                                self.__class__.__name__,
        #                                representation)

    def __getattribute__(self, attribute: str) -> Any:
        """

        :param attribute:
        :type attribute: str

        :return:
        :rtype: Any
        """
        try:
            return super().__getattribute__(attribute)
        except AttributeError as error:
            if attribute.startswith("add"):
                look_up = attribute.split("add_")[-1]
                if look_up:
                    class_ = MatrixNodeCollection.registry[look_up]
                    return partial(self.add_custom_child, class_)
                else:
                    raise error
            else:
                raise error

    # @staticmethod
    # @abstractmethod
    # def type() -> str:
    #     """

    #     :return:
    #     :rtype: str
    #     """

    # def to_json(self) -> Dict:
    #     """

    #     :return:
    #     :rtype: dict
    #     """
    #     return {"content": [entity.to_json() for entity in self]}

    def is_ordered(self) -> bool:
        """

        :return:
        :rtype: bool
        """
        return True

    def allows_selection(self) -> bool:
        """

        :return:
        :rtype: bool
        """
        return False

    def append(self, node: Union[MatrixNode, "MatrixNodeCollection"]):
        """

        :param node:
        :type node: `morphologicalmatrix.matrixnode.MatrixNode` or
            `morphologicalmatrix.matrixnodecollection.MatrixNodeCollection`

        :raises TypeError: Raised if the supplied node data type is not valid
        """
        if not isinstance(node, (MatrixNodeCollection, MatrixNode, )):
            raise TypeError("Unsupported data type for 'append' operation.")
        if not node.parent() == self:
            node._parent = self
        return super().append(node)

    def insert(self, position: int, node: MatrixNode):
        """

        :param position:
        :type position: int

        :param node:
        :type node: `morphologicalmatrix.matrixnode.MatrixNode` or
            `morphologicalmatrix.matrixnodecollection.MatrixNodeCollection`

        :raises TypeError: Raised if the supplied node data type is not valid
        """
        if not isinstance(node, (MatrixNodeCollection, MatrixNode, )):
            raise TypeError("Unsupported data type for 'insert' operation.")
        if not node.parent() == self:
            node._parent = self
        return super().insert(position, node)

    def remove(self, node: MatrixNode):
        """

        :param node:
        :type node: `morphologicalmatrix.matrixnode.MatrixNode` or
            `morphologicalmatrix.matrixnodecollection.MatrixNodeCollection`

        :raises TypeError: Raised if the supplied node data type is not valid
        """
        if not isinstance(node, (MatrixNodeCollection, MatrixNode, )):
            raise TypeError("Unsupported data type for 'remove' operation.")
        return super().remove(node)

    def extend(self, node_collection: "MatrixNodeCollection"):
        """

        :param node_collection:
        :type node_collection: `{0}.{1}`

        :raises TypeError: Raised if the supplied collection data type is not
            valid
        """.format(self.__class__.__module__, self.__class__.__name__)
        if not isinstance(node_collection, MatrixNodeCollection):
            raise TypeError("Unsupported data type for 'extend' operation.")
        return super().extend(node_collection)

    def entity(self, name: str, start: Optional[int]=None,
               end: Optional[int]=None) -> Optional[MatrixNode]:
        """

        :param name:
        :type name: str

        :param start: default None
        :type start: int

        :param end: default None
        :type end: int

        :return:
        :rtype: `morphologicalmatrix.matrixnode.MatrixNode` or
            `morphologicalmatrix.matrixnodecollection.MatrixNodeCollection`

        :raises ValueError: Raised if the supplied name is not found in the
            collection
        """
        if not start:
            start = 0
        if not end:
            end = len(self)
        for i in range(start, end):
            if self[i].get_name() == name:
                return self[i]
        else:
            raise ValueError("Entry with name %s not found." % name)

    def index(self, node: Union[MatrixNode, "MatrixNodeCollection"],
              start: Optional[int]=None, end: Optional[int]=None) -> int:
        """

        :param node:
        :type node: `morphologicalmatrix.matrixnode.MatrixNode` or
            `morphologicalmatrix.matrixnodecollection.MatrixNodeCollection`

        :param start: default None
        :type start: int

        :param end: default None
        :type end: int

        :return:
        :rtype: int

        :raises TypeError: Raised if the supplied node data type is not valid
        """
        if not isinstance(node, (MatrixNodeCollection, MatrixNode, )):
            raise TypeError("Unsupported data type for 'index' operation.")
        return super().index(node, start, end)

    def count(self, node: Union[MatrixNode, "MatrixNodeCollection"]) -> int:
        """

        :param node:
        :type node: `morphologicalmatrix.matrixnode.MatrixNode` or
            `morphologicalmatrix.matrixnodecollection.MatrixNodeCollection`

        :return:
        :rtype: int

        :raises TypeError: Raised if the supplied node data type is not valid
        """
        if not isinstance(node, (MatrixNodeCollection, MatrixNode, )):
            raise TypeError("Unsupported data type for 'count' operation.")
        return super().count(node)

    def options_count(self) -> int:
        """

        :return:
        :rtype: int
        """
        return len(self.options())

    def options(self) -> List[MatrixNode]:
        """

        :return:
        :rtype: list of `morphologicalmatrix.matrixnode.MatrixNode`
        """
        options = []
        for member in self:
            if isinstance(member, list):
                options.extend(member.options())
            else:
                options.append(member)
        return options

    def add_custom_child(self, callable_class: Callable,
                         child: Union["MatrixNodeCollection",
                                      "MatrixNode", str], **kwargs):
        """

        :param callable_class:
        :type callable_class: Callable

        :param child:
        :type child: `morphologicalmatrix.matrixnode.MatrixNode` or str or
            `morphologicalmatrix.matrixnodecollection.MatrixNodeCollection`

        :param kwargs:
        :type kwargs: dict
        """
        if isinstance(child, str):
            child = callable_class(child, self, **kwargs)
        self.append(child)

    @classmethod
    def register_child(cls, child_class: Callable, look_up_name: str):
        """

        :param child_class:
        :type child_class: callable class object

        :param look_up_name:
        :type look_up_name: str

        :raises TypeError: Raised if the supplied component class is not a
            subclass of the `morphologicalmatrix.matrixnode.MatrixNode` or
            `morphologicalmatrix.matrixnodecollection.MatrixNodeCollection`
            base classes
        """
        if not issubclass(child_class, (MatrixNode, MatrixNodeCollection, )):
            raise TypeError("Supplied child class is not a subclass of the "
                            "MatrixNode or MatrixNodeCollection base classes.")
        cls.registry.update({look_up_name: child_class})

    # @classmethod
    # def from_json(self, content: List["MatrixNode"]):
    #     """

    #     :param content:
    #     :type content: dict
    #     """
    #     from .subsystem import SubSystem
    #     from .component import Component

