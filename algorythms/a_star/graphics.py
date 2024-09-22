"""Обработка визуального отображения метода A*."""

from ..base import Graphic
from .map import AStarMap


class AStarGraphic(Graphic[AStarMap]):
    """Обработчик визуального отображения метода A*."""

    MAP_TYPE = AStarMap
