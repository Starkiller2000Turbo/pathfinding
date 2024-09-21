"""Обработка визуального отображения карты."""

from functools import wraps
from traceback import format_exc
from typing import Callable, Generic, Optional, Type, TypeVar

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backend_bases import Event, MouseButton, MouseEvent
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from matplotlib.widgets import Button, TextBox
from typing_extensions import Concatenate, ParamSpec

from .exceptions import WrongActionError
from .logging import logger
from .map import Map
from .math_handlers import Point

DecParams = ParamSpec('DecParams')
RetVar = TypeVar('RetVar')


def handle_error(message: str = '') -> Callable[
    [Callable[Concatenate['Graphic', DecParams], RetVar]],
    Callable[Concatenate['Graphic', DecParams], Optional[RetVar]],
]:
    """Обработать исключение при обработке взаимодействия с графическими элементами.

    Returns:
        Декоратор функции.
    """

    def decorate(
        function: Callable[Concatenate['Graphic', DecParams], RetVar],
    ) -> Callable[Concatenate['Graphic', DecParams], Optional[RetVar]]:

        @wraps(function)
        def wrapper(self: 'Graphic', *args: DecParams.args, **kwargs: DecParams.kwargs) -> Optional[RetVar]:
            self.clear_exception()
            try:
                return function(self, *args, **kwargs)
            except Exception as ex:
                logger.error(format_exc())
                if message:
                    self.perform_exception(WrongActionError(f'{message}\n{str(ex)}'))
                else:
                    self.perform_exception(WrongActionError(str(ex)))
                return None

        return wrapper

    return decorate


MapType = TypeVar('MapType', bound=Map)


class Graphic(Generic[MapType]):
    """Обработчик визуального отображения карты."""

    fig: Figure
    ax: Axes
    event_id: int
    MAP_TYPE: Type[MapType] = Map  # type: ignore[assignment]
    data: AxesImage

    def __init__(self, width: int = 10, height: int = 10) -> None:
        """Инициализировать обработчик визуального отображения карты.

        Args:
            width: задаваемая ширина лабиринта.
            height: задаваемая высота лабиринта.
        """
        self.map = self.MAP_TYPE()
        self.map.width = width
        self.map.height = height

    def delete_start_arrow(self) -> None:
        """Удалить начальньную точку лабиринта."""
        if hasattr(self, 'start_arrow'):
            self.start_arrow.remove()
            del self.start_arrow
            self.map.start_point = None

    def delete_end_arrow(self) -> None:
        """Удалить конечную точку лабиринта."""
        if hasattr(self, 'end_arrow'):
            self.end_arrow.remove()
            del self.end_arrow
            self.map.end_point = None

    def delete_path(self) -> None:
        """Удалить путь."""
        if hasattr(self, 'path'):
            for line in self.path:
                line.remove()
            del self.path
            self.map.clear()

    @handle_error('Не удалось выбрать положение начальной точки')
    def on_click_after_start(self, event: Event) -> None:
        """Обработка нажатия на карту после нажатия на кнопку "Задать начальную точку".

        Args:
            event: событие клика.
        """
        if isinstance(event, MouseEvent):
            if event.button is MouseButton.LEFT:
                if not event.xdata or not event.ydata:
                    raise WrongActionError('Нажата точка за пределами поля')
                point = Point(round(event.xdata), round(event.ydata))
                self.map.start_point = point
                self.start_arrow = self.ax.arrow(
                    point.x - 0.4,
                    point.y,
                    0.5,
                    0,
                    fc='green',
                    ec='green',
                    head_width=0.3,
                    head_length=0.3,
                )
                plt.show()
                plt.disconnect(self.event_id)

    @handle_error('Не удалось выбрать положение конечной точки')
    def on_click_after_end(self, event: Event) -> None:
        """Обработка нажатия на карту после нажатия на кнопку "Задать конечную точку".

        Args:
            event: событие клика.
        """
        if isinstance(event, MouseEvent):
            if event.button is MouseButton.LEFT:
                if not event.xdata or not event.ydata:
                    raise WrongActionError('Нажата точка за пределами поля')
                point = Point(round(event.xdata), round(event.ydata))
                self.map.end_point = point
                self.end_arrow = self.ax.arrow(
                    point.x - 0.4,
                    point.y,
                    0.5,
                    0,
                    fc='blue',
                    ec='blue',
                    head_width=0.3,
                    head_length=0.3,
                )
                plt.show()
                plt.disconnect(self.event_id)

    @handle_error('Не удалось нажать на кнопку задания начального положения')
    def click_start_button(self, event: Event) -> None:
        """Обработка нажатия на кнопку "Задать начальную точку".

        Args:
            event: событие клика.
        """
        if hasattr(self, 'event_id'):
            plt.disconnect(self.event_id)
        self.delete_start_arrow()
        self.delete_path()
        plt.show()
        self.event_id = plt.connect('button_press_event', self.on_click_after_start)

    @handle_error('Не удалось нажать на кнопку задания конечного положения')
    def click_end_button(self, event: Event) -> None:
        """Обработка нажатия на кнопку "Задать конечную точку".

        Args:
            event: событие клика.
        """
        if hasattr(self, 'event_id'):
            plt.disconnect(self.event_id)
        self.delete_end_arrow()
        self.delete_path()
        plt.show()
        self.event_id = plt.connect('button_press_event', self.on_click_after_end)

    @handle_error('Не удалось нажать на кнопку очистки карты')
    def click_clear(self, event: Event) -> None:
        """Обработка нажатия на кнопку "Очистить".

        Args:
            event: событие клика.
        """
        self.delete_start_arrow()
        self.delete_end_arrow()
        self.delete_path()
        plt.show()

    @handle_error('Не удалось задать количество строк')
    def x_change(self, event: Event) -> None:
        """Обработка задания текста в поле "Кол-во строк".

        Args:
            event: событие.
        """
        try:
            self.map.width = self.x_input.text
        except Exception as ex:
            self.x_input.set_val(self.map.width)
            raise ex

    @handle_error('Не удалось задать количество столбцов')
    def y_change(self, event: Event) -> None:
        """Обработка задания текста в поле "Кол-во столбцов".

        Args:
            event: событие.
        """
        try:
            self.map.height = self.y_input.text
        except Exception as ex:
            self.y_input.set_val(self.map.height)
            raise ex

    def plot_map(self) -> None:
        """Вывести карту."""
        self.map.generate_map()
        self.ax.cla()
        self.error_text = self.ax.text(
            0.5,
            -0.05,
            '',
            transform=self.ax.transAxes,
            style='italic',
            horizontalalignment='center',
            verticalalignment='top',
            bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10},
        )
        self.data = self.ax.imshow(
            [[0 if cell.passable else 1 for cell in row] for row in self.map.data.data],
            cmap=plt.cm.binary,  # type: ignore[attr-defined]
            interpolation='none',
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        plt.show()

    @handle_error('Не удалось изменить карту')
    def map_change(self, event: Event) -> None:
        """Обработка нажатия на кнопку "Изменить карту".

        Args:
            event: событие клика.
        """
        self.click_clear(event)
        self.plot_map()

    @handle_error('Не удалось обнаружить путь')
    def find_path(self, event: Event) -> None:
        """Обработка нажатия на кнопку "Найти путь".

        Args:
            event: событие клика.
        """
        self.delete_path()
        path = self.map.find_path()
        self.path = self.ax.plot([point.x for point in path], [point.y for point in path])
        plt.show()

    def draw_maze(self):
        """Отобразить лабиринт."""
        self.fig, self.ax = plt.subplots(figsize=(10, 10))

        # Управляющие кнопки
        RIGHT_POSITION = 0.9
        WIDTH = 0.1
        HEIGHT = 0.075
        MIDDLE_POSITION = 0.5

        axstart = self.fig.add_axes([RIGHT_POSITION, MIDDLE_POSITION + 0.25, WIDTH, HEIGHT])
        axend = self.fig.add_axes([RIGHT_POSITION, MIDDLE_POSITION, WIDTH, HEIGHT])
        axclear = self.fig.add_axes([RIGHT_POSITION, MIDDLE_POSITION - 0.25, WIDTH, HEIGHT])
        self.start_button = Button(axstart, 'Задать\nначальную\nточку')
        self.start_button.on_clicked(self.click_start_button)
        self.end_button = Button(axend, 'Задать\nконечную\nточку')
        self.end_button.on_clicked(self.click_end_button)
        self.clear_button = Button(axclear, 'Очистить')
        self.clear_button.on_clicked(self.click_clear)

        # Поля ввода
        LEFT_POSITION = 0

        ax_x_input = self.fig.add_axes([LEFT_POSITION, MIDDLE_POSITION + 0.3, WIDTH, HEIGHT])
        ax_y_input = self.fig.add_axes([LEFT_POSITION, MIDDLE_POSITION + 0.1, WIDTH, HEIGHT])
        self.x_input = TextBox(ax_x_input, 'Кол-во\nстрок:', '10', textalignment='center')
        x_label = self.x_input.ax.get_children()[0]
        x_label.set_position([0.5, 1.5])
        x_label.set_verticalalignment('top')
        x_label.set_horizontalalignment('center')
        self.x_input.on_submit(self.x_change)
        self.y_input = TextBox(ax_y_input, 'Кол-во\nстолбцов:', '10', textalignment='center')
        self.y_input.on_submit(self.y_change)
        y_label = self.y_input.ax.get_children()[0]
        y_label.set_position([0.5, 1.5])
        y_label.set_verticalalignment('top')
        y_label.set_horizontalalignment('center')

        # кнопки управления картой
        ax_map_rebuild = self.fig.add_axes([LEFT_POSITION, MIDDLE_POSITION - 0.1, WIDTH, HEIGHT])
        self.map_rebuild_button = Button(ax_map_rebuild, 'Изменить\nкарту')
        self.map_rebuild_button.on_clicked(self.map_change)

        # кнопки управления алгоритмом
        ax_find_path = self.fig.add_axes([LEFT_POSITION, MIDDLE_POSITION - 0.3, WIDTH, HEIGHT])
        self.find_path_button = Button(ax_find_path, 'Найти\nпуть')
        self.find_path_button.on_clicked(self.find_path)

        # Текстовое поле с ошибкой
        self.plot_map()

    def perform_exception(self, exception: Exception) -> None:
        """Выполнить в случае вызова исключения.

        Args:
            exception: выполнить в случае исключения.
        """
        self.error_text.set_text(str(exception))
        plt.show()

    def clear_exception(self) -> None:
        """Очистить сообщение об исключении."""
        self.error_text.set_text('')
        plt.show()
