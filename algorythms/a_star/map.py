"""Обработка карты c алгоритмом А*."""

from typing import List

from ..base import DIRECTIONS, Map
from ..base.exceptions import CalculationFailedError, DataNotProvidedError
from ..base.math_handlers import Point


class AStarMap(Map):
    """Карта волнового метода, содержащая проходимые и непроходимые точки."""

    def find_path(self) -> List[Point]:
        """Найти путь в лабиринте.

        Returns:
            Список точек.
        """
        self.clear()
        if not hasattr(self, 'data'):
            raise DataNotProvidedError('Не задано поле')
        if not self.start_point:
            raise DataNotProvidedError('Не задана начальная точка')
        if not self.end_point:
            raise DataNotProvidedError('Не задана конечная точка')
        points = [self.start_point]
        self.data[self.start_point].distance = 0
        path_found = False
        while points and not path_found:
            point = points[0]
            if point == self.end_point:
                path_found = True
            for direction in DIRECTIONS:
                new_point = point + direction
                if self.data[new_point].passable and self.data[new_point].distance is None and new_point not in points:
                    points.append(new_point)
                    self.data[new_point].distance = self.data[point].distance + 1  # type: ignore[operator]
            points.remove(point)
            points = sorted(points, key=self.evtistic_function)
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

    def evtistic_function(self, point: Point) -> int:
        """Рассчитать эвристичечкую функцию для заданной точки.

        Args:
            point: точка, для которой необходимо рассчитать функцию.

        Returns:
            Значение эвристической функции (квадрат расстояния до точки).
        """
        if not self.end_point:
            raise DataNotProvidedError('Не задана конечная точка')
        return (self.end_point.x - point.x) ** 2 + (self.end_point.y - point.y) ** 2
