"""
    :author: inunarun
             Aerospace Systems Design Laboratory,
             Georgia Institute of Technology,
             Atlanta, GA

    :date: 2018-04-15 15:18:32
"""

from typing import Callable, Tuple, Union, Dict, List
import numpy as np


class CompatibilityMatrix(np.ndarray):
    """

    """

    def __new__(cls: Callable,
                shape: Tuple[int, int]) -> "CompatibilityMatrix":
        """

        :param cls:
        :type cls:

        :param shape:
        :type shape: tuple of (int, int)

        :return:
        :rtype: `morphologicalmatrix.compatibilitymatrix.CompatibilityMatrix`
        """
        return np.asarray(np.identity(shape, dtype=int)).view(cls)

    def __setitem__(self, indices: Tuple[int, int],
                    value: Union[int, np.ndarray]):
        """

        :param indices:
        :type indices: tuple of int

        :param value:
        :type value: int or np.ndarray
        """
        if isinstance(value, int):
            if value not in [0, 1]:
                raise ValueError("Compatibility value has to be 0 or 1.")
        else:
            if (value.size and
                not np.all(np.logical_or(value == 0, value == 1))):
                raise ValueError("Compatibility value has to be 0 or 1.")

        i, j = indices
        super().__setitem__((i, j), value)
        super().__setitem__((j, i), value)

    def reinitialize_from(self, old_matrix: np.ndarray):
        """

        :param old_matrix:
        :type old_matrix: np.ndarray
        """
        self[:old_matrix.shape[0], :old_matrix.shape[1]] = old_matrix

    def evaluate_compatibility(self, selection: List["MatrixNode"]) -> bool:
        """

        :param selection:
        :type selection: list of `morphologicalmatrix.matrixnode.MatrixNode`

        :return:
        :rtype: bool
        """
        state_vector = np.zeros((self.shape[0], ))
        for component in selection:
            state_vector[component.index()] = 1.
        for component in selection:
            compatiblity = component.get_compatibilities()
            compatibility_value = np.dot(1 - state_vector, compatiblity)
            if compatibility_value >= 1:
                return False

        else:
            return True

    # def to_json(self) -> Dict:
    #     """

    #     :return:
    #     :rtype: dict
    #     """
    #     return {
    #         "contents": self.tolist(),
    #     }

    # @classmethod
    # def from_json(cls, content: List[List]):
    #     """

    #     :param content:
    #     :type content: dict
    #     """
    #     matrix = CompatibilityMatrix(len(content))
    #     matrix.reinitialize_from(np.array(content))
    #     return matrix
