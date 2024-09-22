## Визуализатор алгоритмов поиска пути
### Описание:

Визуализатор поиска пути с ипользованием различных алгоритмов 

Проект создан в рамках знакомства с пакетом [`Matplotlib`](https://pypi.org/project/matplotlib/) и различными методами поиска пути. Поэтому реализован без использования других библиотек

Реализован алгоритм генерации лабиринтов

Реализованы следующие методы поиска пути:

- [Волновой алгоритм](https://ru.wikipedia.org/wiki/%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D0%9B%D0%B8)
- [Алгоритм А*](https://ru.wikipedia.org/wiki/A*) (функция - расстояние до точки)


### Как запустить проект:

Клонируйте репозиторий:
```commandline
git clone git@github.com:Starkiller2000Turbo/pathfinding.git
```

Измените свою текущую рабочую дерикторию:
```commandline
cd pathfinding
```

Создайте и активируйте виртуальное окружение

```commandline
python -m venv venv
source venv/Scripts/activate
```

Обновите pip и установите зависимости из requirements.txt:
```commandline
make req
```

### Запустить проект

Запустить волновой алгоритм:
```commandline
make wave
```

### Проверка стиля кода

Для проверки стиля кода необходимо установить необходимые зависимости и запустить соответствующий скрипт:

```
make style_req
make style
```

### Авторы:

- [`Starkiller2000Turbo`](https://github.com/Starkiller2000Turbo)

### Стек технологий использованный в проекте:

#### Основная часть

- [`Python`](https://www.python.org/)
- [`Matplotlib`](https://pypi.org/project/matplotlib/)

#### Стиллизация
 
- [`Isort`](https://pypi.org/project/isort/)
- [`Black`](https://pypi.org/project/black/)
- [`Flake8`](https://pypi.org/project/flake8/)
- [`Flake8-commas`](https://pypi.org/project/flake8-commas/)
- [`Flake8-docstrings`](https://pypi.org/project/flake8-docstrings/)
- [`Flake8-print`](https://pypi.org/project/flake8-print/)
- [`Flake8-pyproject`](https://pypi.org/project/flake8-pyproject/)
- [`Flake8-quotes`](https://pypi.org/project/flake8-quotes/)
- [`Mypy`](https://pypi.org/project/mypy/)