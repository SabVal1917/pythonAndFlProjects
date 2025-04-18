# TP Project Chess 2024

## Запуск
Для запуска игры необходимо подключить оба компьютера к одной WiFi сети.
После этого запускаем игру:

```./main.py```

Появится запрос на выбор запуска сервера или клиента.
На одном устройстве пишем ```server / s```, после чего должен
появиться адрес запущенного сервера.
На другом устройстве пишем ```client / c``` и вводим полученный адрес.

После описанных действий игра должна начаться.

## Управление

Игрок, который ходит белыми фигурами, начинает игру. Игроки делают ходы по очереди.

Выберите фигуру, нажав левой кнопкой мыши на нее. Затем выберите клетку, куда хотите переместить фигуру. Если ход разрешен, фигура переместится на новую клетку.

## Правила игры

Игра ведется на шахматной доске 8x8 клеток. Цель игры - поставить мат королю противника.

Фигуры ходят следующим образом:

* Пешка ходит на одну клетку вперед или бьет на одну клетку вперед по диагонали.
* Конь ходит буквой "Г" - на две клетки в любом направлении, а затем на одну клетку в перпендикулярном направлении.
* Слон ходит по диагонали на любое количество клеток.
* Ладья ходит по горизонтали или вертикали на любое количество клеток.
* Ферзь может ходить как слон, так и ладья.
* Король ходит на одну клетку в любом направлении.

## Требования
* Python 3.x
* Модули Python из файла requirements.txt

## Разработчики проекта
* Кормин Павел Б05-325
* Хомяков Максимилиан Б05-325
