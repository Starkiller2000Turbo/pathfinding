"""Обработка визуального отображения волнового метода."""

from ..base import Graphic
from .map import WaveMap


class WaveGraphic(Graphic[WaveMap]):
    """Обработчик визуального отображения волнового метода."""

    MAP_TYPE = WaveMap
