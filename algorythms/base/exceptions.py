"""Ошибки при работе с интерфейсом и классами обработчиков."""


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
    """Не удалось рассчитать."""

    pass
