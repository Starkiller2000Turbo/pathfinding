"""Обработка математических составляющих."""

from typing import Generic, Iterator, List, TypeVar

from .exceptions import WrongArgumentValuesError


class Vector:
    """Класс для обработки вектора."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализировать вектор.

        Args:
            x: позиция вектора по оси x.
            y: позиция вектора по оси y.
        """
        self.x = x
        self.y = y


class Point:
    """Класс для обработки точки."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализировать точку.

        Args:
            x: позиция точки по оси x.
            y: позиция точки по оси y.
        """
        self.x = x
        self.y = y

    def __add__(self, vector: Vector) -> 'Point':
        """Прибавление вектора к точке.

        Args:
            Прибавляемый вектор.

        Returns:
            Точку с прибавленными значениями координат согласно вектору.
        """
        if not isinstance(vector, Vector):
            raise WrongArgumentValuesError('К точке можно прибавлять только вектор')

        return Point(self.x + vector.x, self.y + vector.y)

    def __mul__(self, number: int) -> 'Point':
        """Умножить точку на число.

        Args:
            number: число, на которое необходимо умножить координаты точки.

        Returns:
            Точку, координаты которой умножены на заданное число.
        """
        if not isinstance(number, int):
            raise WrongArgumentValuesError('Точку можно умножать только на число')

        return Point(self.x * number, self.y * number)

    def __iter__(self) -> Iterator[int]:
        """Итерировать координаты точки.

        Returns:
            Координаты x и y последовательно.
        """
        yield self.x
        yield self.y

    def __eq__(self, value: object) -> bool:
        """Сравнить точку с другой точкой.

        Args:
            value: сравниваемое значение.

        Returns:
            Логическое значение, являются ли точки равными.
        """
        return isinstance(value, Point) and value.x == self.x and value.y == self.y

    def __repr__(self) -> str:
        """Получить строковое представление точки.

        Returns:
            Строку с координатами точки.
        """
        return f'Точка ({self.x}, {self.y})'


CellVar = TypeVar('CellVar')


class Matrix(Generic[CellVar]):
    """Обработчик матрицы с переменным типом содержимого."""

    def __init__(self, data: List[List[CellVar]]) -> None:
        """Инициализировать обработчик матрицы.

        Args:
            data: тип используемого содержимого.
        """
        self.data = data

    def __getitem__(self, point: Point) -> CellVar:
        """Получить элемент из матрицы по точке.

        Args:
            point: точка, координаты которой совпадают с координатами желаемого значения.

        Returns:
            Значение по заданным координатам.
        """
        return self.data[point.y][point.x]

    def __setitem__(self, point: Point, value: CellVar) -> None:
        """Задать значение элементу матрицы по точке.

        Args:
            point: точка, координаты которой совпадают с координатами желаемого значения.
            value: желаемое значение, которое необходимо разместить в ячейку.
        """
        self.data[point.y][point.x] = value

    def __iter__(self) -> Iterator[List[CellVar]]:
        """Получить итератор матрицы.

        Returns:
            Итератор хранимого списка.
        """
        return self.data.__iter__()
