"""Обработка карты."""

from typing import List

from ..base import DIRECTIONS, Map
from ..base.exceptions import CalculationFailedError, DataNotProvidedError
from ..base.math_handlers import Point


class WaveMap(Map):
    """Карта волнового метода, содержащая проходимые и непроходимые точки."""

    def find_path(self) -> List[Point]:
        """Найти путь в лабиринте.

        Returns:
            Список точек.
        """
        if not hasattr(self, 'data'):
            raise DataNotProvidedError('Не задано поле')
        if not self.start_point:
            raise DataNotProvidedError('Не задана начальная точка')
        if not self.end_point:
            raise DataNotProvidedError('Не задана конечная точка')
        distance = 0
        points = [self.start_point]
        path_found = False
        while points and not path_found:
            new_points = []
            for point in points:
                if point == self.end_point:
                    path_found = True
                self.data[point].distance = distance
                for direction in DIRECTIONS:
                    new_point = point + direction
                    if (
                        self.data[new_point].passable
                        and not self.data[new_point].passed
                        and new_point not in new_points
                    ):
                        new_points.append(new_point)
                self.data[point].passed = True
            points = new_points
            distance += 1
        if not path_found:
            raise CalculationFailedError('Не удалось найти путь')
        path = [self.end_point]
        point = self.end_point
        while not point == self.start_point:
            for direction in DIRECTIONS:
                new_point = point + direction
                if self.data[new_point].distance == self.data[point].distance - 1:  # type: ignore[operator]
                    path.append(new_point)
                    point = new_point
                    break
        return path
