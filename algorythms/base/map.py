"""Обработка карты."""

import random
from typing import Any, List, Optional

from .exceptions import DataNotProvidedError, WrongArgumentValuesError
from .math_handlers import Matrix, Point, Vector

DIRECTIONS = [Vector(0, 1), Vector(1, 0), Vector(0, -1), Vector(-1, 0)]


class MapPoint:
    """Обработчик точки в карте."""

    def __init__(self, passable: bool, distanse: Optional[int] = None, passed: bool = False):
        """Инициализировать обработчик точки в карте.

        Args:
            passable: проходимая ли точка.
            distanse: расстояние от начальной точки.
        """
        self.distance = distanse
        self.passable = passable
        self.passed = passed

    def clear(self) -> None:
        """Очистить ячейку таблицы."""
        self.distance = None
        self.passed = False


class Map:
    """Карта, содержащая проходимые и непроходимые точки."""

    data: Matrix[MapPoint]
    _n: int
    _m: int
    _start_point: Optional[Point] = None
    _end_point: Optional[Point] = None
    _height: int
    _width: int
    path: List[Point]

    @property
    def start_point(self) -> Optional[Point]:
        """Получить значение начальной точки.

        Returns:
            Обработчик Point для описания начальной точки.
        """
        return self._start_point

    @start_point.setter
    def start_point(self, point: Optional[Point]) -> None:
        """Задать значение начальной точке.

        Args:
            point: значение начальной точки.
        """
        if point:
            if not hasattr(self, 'data'):
                raise DataNotProvidedError('Карта ещё не сгенерирована')
            if not self.data[point].passable:
                raise WrongArgumentValuesError('Выбрана непроходимая точка')
        self._start_point = point

    @property
    def end_point(self) -> Optional[Point]:
        """Получить значение конечной точки.

        Args:
            point: значение конечной точки.
        """
        return self._end_point

    @end_point.setter
    def end_point(self, point: Optional[Point]) -> None:
        """Задать значение конечной точке.

        Args:
            point: значение конечной точки.
        """
        if point:
            if not hasattr(self, 'data'):
                raise DataNotProvidedError('Карта ещё не сгенерирована')
            if not self.data[point].passable:
                raise WrongArgumentValuesError('Выбрана непроходимая точка')
        self._end_point = point

    @property
    def height(self) -> int:
        """Получить значение высоты.

        Returns:
            Целое число, соответствующее количеству строк лабиринта.
        """
        return self._height

    @height.setter
    def height(self, value: Any) -> None:
        """Задать значение высоты лабиринта.

        Args:
            value: значение высоты лабиринта.
        """
        try:
            int_value = int(value)
        except ValueError:
            raise WrongArgumentValuesError(f'Неверное значение ввода: "{value}". Должно быть целое число')
        if int_value < 1:
            raise WrongArgumentValuesError('Значение должно быть больше 0')
        self._height = int_value

    @property
    def width(self) -> int:
        """Получить значение ширины.

        Returns:
            Целое число, соответствующее количеству столбцов лабиринта.
        """
        return self._width

    @width.setter
    def width(self, value: Any) -> None:
        """Задать значение ширины лабиринта.

        Args:
            value: значение ширины лабиринта.
        """
        try:
            int_value = int(value)
        except ValueError:
            raise WrongArgumentValuesError(f'Неверное значение ввода: "{value}". Должно быть целое число')
        if int_value < 1:
            raise WrongArgumentValuesError('Значение должно быть больше 0')
        self._width = int_value

    def generate_map(self) -> None:
        """Сгенерировать карту."""
        self._n = 2 * self.height + 1
        self._m = 2 * self.width + 1
        self.data = Matrix([[MapPoint(passable=False) for _ in range(self._m)] for _ in range(self._n)])

        stack = [Point(0, 0)]
        while len(stack) > 0:
            point = stack[-1]
            random.shuffle(DIRECTIONS)

            for direction in DIRECTIONS:
                next_point = point + direction
                if (
                    next_point.x >= 0
                    and next_point.y >= 0
                    and next_point.x < self.width
                    and next_point.y < self.height
                    and not self.data[self.to_raw(next_point)].passable
                ):
                    self.data[self.to_raw(next_point)].passable = True
                    self.data[self.to_raw(point) + direction].passable = True
                    stack.append(next_point)
                    break
            else:
                stack.pop()

    def __repr__(self) -> str:
        """Получить строковое предсавление карты.

        Returns:
            Строковое представление в виде черных и белых квадратов.
        """
        return '\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.data])

    @staticmethod
    def to_raw(point: Point) -> Point:
        """Преобразовать координаты точки в грубые координаты внутри лабиринта.

        Returns:
            Точку с преобразованными координатами.
        """
        return point * 2 + Vector(1, 1)

    def find_path(self) -> List[Point]:
        """Найти путь в лабиринте.

        Returns:
            Список точек.
        """
        return []

    def clear(self) -> None:
        """Очистить данные всех точек."""
        for row in self.data:
            for cell in row:
                cell.clear()
