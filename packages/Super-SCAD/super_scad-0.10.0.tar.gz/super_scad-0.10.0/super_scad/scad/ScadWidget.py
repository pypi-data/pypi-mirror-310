import typing
from abc import ABC, abstractmethod
from typing import Any, List

from super_scad.scad import Length
from super_scad.scad.Context import Context
from super_scad.scad.Unit import Unit
from super_scad.type.Vector2 import Vector2
from super_scad.type.Vector3 import Vector3

ScadWidget = typing.NewType('ScadWidget', None)


class ScadWidget(ABC):
    """
    Abstract parent widget for all SuperSCAD widgets.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, ):
        """
        Object constructor.
        """

        self.__unit: Unit = Context.get_unit_length_current()
        """
        The unit of length of the Context of this OpenSCAD widget.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def uc(self, length: Any) -> Any:
        """
        Returns the length in the unit of the current context.

        :param length: The length.
        """
        if Context.get_unit_length_current() == self.__unit:
            if isinstance(length, int):
                return float(length)
            return length

        if length is None:
            return None

        if isinstance(length, float):
            return Length.convert(length, self.__unit, Context.get_unit_length_current())

        if isinstance(length, int):
            return Length.convert(float(length), self.__unit, Context.get_unit_length_current())

        if isinstance(length, Vector2):
            return Vector2(self.uc(length.x), self.uc(length.y))

        if isinstance(length, Vector3):
            return Vector3(self.uc(length.x), self.uc(length.y), self.uc(length.z))

        if isinstance(length, List):
            return [self.uc(point) for point in length]

        raise ValueError('Can not convert length of type {}.'.format(type(length)))

# ----------------------------------------------------------------------------------------------------------------------
