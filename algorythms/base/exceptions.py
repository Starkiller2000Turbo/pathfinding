"""Ошибки для остановки процесса."""


class WrongArgumentValuesError(Exception):
    """Неверное значение входных данных."""

    pass


class DataNotProvidedError(Exception):
    """Не задана начальная точка."""

    pass


class WrongActionError(Exception):
    """Проводится неверная операция."""

    pass


class CalculationFailedError(Exception):
    """Неудалось рассчитать."""

    pass
