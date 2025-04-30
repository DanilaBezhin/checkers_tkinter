# board.py
import tkinter as tk
from checker import Checker
from var import *

class CheckersBoard:
    """
    Инициализирует объект CheckersBoard.

    Параметры
    ---------
    root : Tk
        Основное окно приложения, которое используется для отображения игрового поля.
    
    Атрибуты
    ---------
    cell_size : int
        Размер одной клетки на доске.
    canvas : Canvas
        Объект Canvas для рисования доски и шашек.
    checker_position : list
        Двумерный список, представляющий начальное положение шашек на доске.
    checkers : list
        Список для хранения объектов шашек.
    """
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.cell_size = 100
        self.canvas = tk.Canvas(self.root, width=8*self.cell_size, height=8*self.cell_size)
        self.canvas.pack()
        self.checker_position = [
            ["_", "B", "_", "B", "_", "B", "_", "B"],
            ["B", "_", "B", "_", "B", "_", "B", "_"],
            ["_", "B", "_", "B", "_", "B", "_", "B"],
            ["_", "_", "_", "_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_", "_", "_", "_"],
            ["W", "_", "W", "_", "W", "_", "W", "_"],
            ["_", "W", "_", "W", "_", "W", "_", "W"],
            ["W", "_", "W", "_", "W", "_", "W", "_"],
        ]
        self.canvas.bind('<Button-1>', self.click_on_board)
        self.is_animation = False
        self.current_player = "white"
        self.color_mapping = {
            "B": "black",
            "W": "white"
        }

        self.create_board()
        self.create_checkers()

    def create_board(self):
        """
        Создает игровую доску для шашек.

        Этот метод отвечает за рисование прямоугольников, представляющих клетки 
        доски. Цвет клеток определяется в зависимости от их координат. Метод 
        использует метод get_cell_color для получения цвета каждой клетки.

        Параметры
        ---------
        Нет параметров для входа, так как функция использует текущие атрибуты объекта.

        Возвращает
        ---------
        Нет.
        """
        for row in range(8):
            for col in range(8):
                cell_color = self.get_cell_color(row, col)
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cell_color)

    def get_cell_color(self, row, col):
        """
        Определяет цвет клетки на доске.

        Метод возвращает цвет клетки в зависимости от её координат. Цвета чередуются,
        чтобы создать шахматный узор для доски шашек. Если сумма индексов строки и
        столбца четная, клетка будет цвета "cornsilk", в противном случае - цвета
        "chocolate4".

        Параметры
        ----------
        row : int
            Индекс строки (от 0 до 7) для определения положения клетки.
        col : int
            Индекс столбца (от 0 до 7) для определения положения клетки.

        Возвращает
        ----------
        str
            Цвет клетки в виде строки, например, "cornsilk" или "chocolate4".
        """
        if (row + col) % 2 == 0:
            return COLOR_LIGHT
        else:
            return COLOR_DARK

    def create_checkers(self):
        """
        Создает шашки на доске в соответствии с начальной конфигурацией.

        Метод проходит по двумерному массиву `checker_position`, который определяет
        начальные позиции шашек. Если клетка содержит "B", создается черная шашка, 
        если "W" — белая шашка. Созданные шашки добавляются на доску.

        Параметры
        ----------
        Нет параметров для входа, так как функция использует атрибуты объекта.

        Возвращает
        ---------
        Нет.
        """
        for row in range(8):
            for col in range(8):
                color = self.checker_position[row][col]
                if color in self.color_mapping:
                    checker = Checker(self, col, row, size=self.cell_size, color=self.color_mapping[color], game=self.game)
                    self.add_checker(checker)

    def add_checker(self, checker):
        """
        Добавляет шашку на доску.

        Метод добавляет переданную шашку в список шашек на доске.

        Параметры
        ----------
        checker : Checker
            Объект шашки, который необходимо добавить на доску.

        Возвращает
        ---------
        Нет.
        """
        if checker not in self.game.checkers:
            self.game.checkers.append(checker)

    def clear_highlight(self):
        """
        Убирает выделение со всех шашек на доске.

        Метод проходит по всем шашкам на доске и удаляет выделение
        у тех шашек, которые в данный момент выделены.

        Параметры
        ----------
        Нет параметров для входа, так как функция использует атрибуты объекта.

        Возвращает
        ---------
        Нет.
        """
        for checker in self.game.checkers:
            if checker.is_highlighted:
                checker.remove_highlight()

    def draw_available_circles(self, positions):
        """
        Рисует кружки на доске в указанных позициях.

        Метод очищает предыдущие выделенные позиции и рисует зеленые кружки,
        указывающие на доступные ходы для выбранной шашки.

        Параметры
        ----------
        positions : list of tuple
            Список позиций (x, y) на доске, где должны быть нарисованы кружки.

        Возвращает
        ---------
        Нет.
        """
        print(f"Зеленные круги будут рисоваться в {positions}")
        self.clear_available_circles()
        if positions:
            for x, y in positions:
                x1 = x * self.cell_size + self.cell_size // 2.3
                y1 = y * self.cell_size + self.cell_size // 2.3
                x2 = x1 + self.cell_size // 6
                y2 = y1 + self.cell_size // 6
                self.canvas.create_oval(x1, y1, x2, y2, fill='yellow', tags='green_circle', outline='')

    def clear_available_circles(self):
        """
        Удаляет все доступные кружки на доске.

        Метод удаляет все зеленые кружки, указывающие на доступные ходы,
        используя тег 'green_circle', чтобы удалить только те объекты, которые
        были отмечены данным тегом.

        Параметры
        ----------
        Нет.

        Возвращает
        ---------
        Нет.
        """
        self.canvas.delete('green_circle')

    def find_active_checker(self):
        """
        Находит активную (выделенную) шашку.

        Метод ищет первую шашку на доске, которая в данный момент выделена, 
        то есть имеет атрибут `is_highlighted`, равный True.

        Параметры
        ----------
        Нет.

        Возвращает
        ---------
        Checker
            Возвращает объект выделенной шашки или None, если выделенной шашки нет.
        """
        for checker in self.game.checkers:
            if checker.is_highlighted:
                return checker
        return None

    def click_on_board(self, event):
        """
        Обрабатывает клик по доске и выполняет действия в зависимости от клика.

        Метод получает координаты клика, определяет клетку на доске и проверяет,
        является ли эта клетка допустимым ходом для активной шашки. Если это обычный
        ход или прыжок через вражескую шашку, то выполняется соответствующее действие.

        Параметры
        ----------
        event : tk.Event
            Событие клика мыши, содержащее координаты клика (event.x и event.y).

        Возвращает
        ---------
        Нет.
        """
        if not self.is_animation:
            col = event.x // self.cell_size
            row = event.y // self.cell_size

            if 0 <= col < 8 and 0 <= row < 8:
                active_checker = self.find_active_checker()

                if active_checker:
                    if active_checker.available_moves and (col, row) in active_checker.available_moves:
                        self.move_checker(col, row)
                        self.game.set_limit_moves()

                    for jump_x, jump_y, enemy_x, enemy_y in active_checker.jump_moves:
                        if (col, row) == (jump_x, jump_y):
                            self.jump_checker(jump_x, jump_y, enemy_x, enemy_y)
                            self.game.set_limit_moves()
    def move_checker(self, col, row):
        """
        Перемещает активную шашку на указанную клетку.

        Метод находит активную шашку и перемещает её на заданную клетку (col, row),
        используя метод `move` объекта шашки.

        Параметры
        ----------
        col : int
            Столбец на доске, куда нужно переместить шашку.
        row : int
            Строка на доске, куда нужно переместить шашку.

        Возвращает
        ---------
        Нет.
        """
        active_checker = self.find_active_checker()
        if active_checker:
            print("обычный ход")
            self.game.count_moves += 1
            active_checker.animate_move(col, row)
            print("смена игрока")
            self.game.switch_player()

    def jump_checker(self, jump_x, jump_y, enemy_x, enemy_y):
        """
        Выполняет прыжок шашки через вражескую шашку и удаляет вражескую шашку.

        Метод перемещает активную шашку на указанную клетку, через которую происходит прыжок,
        и удаляет вражескую шашку, через которую перепрыгнули.

        Параметры
        ----------
        jump_x : int
            Столбец, куда перемещается шашка после прыжка.
        jump_y : int
            Строка, куда перемещается шашка после прыжка.
        enemy_x : int
            Столбец вражеской шашки, через которую осуществляется прыжок.
        enemy_y : int
            Строка вражеской шашки, через которую осуществляется прыжок.

        Возвращает
        ---------
        Нет.
        """
        active_checker = self.find_active_checker()
        if active_checker:
            self.game.count_moves += 1
            active_checker.animate_move(jump_x, jump_y, is_jump=True)
            self.remove_checker(enemy_x, enemy_y)      

    def remove_checker(self, col, row):
        """
        Удаляет шашку с доски.

        Метод находит шашку на указанных координатах и удаляет её из списка шашек,
        а также удаляет её графическое представление на доске.

        Параметры
        ----------
        col : int
            Столбец, где находится шашка, которую нужно удалить.
        row : int
            Строка, где находится шашка, которую нужно удалить.

        Возвращает
        ---------
        Нет.
        """
        checker = self.get_checker_at(col, row)
        if checker:
            self.game.add_captured_checker(checker)
            self.game.checkers.remove(checker)
            self.canvas.delete(checker.oval)

    def get_checker_at(self, x, y):
        """
        Возвращает шашку, находящуюся на указанных координатах.

        Метод ищет шашку в списке `self.game.checkers`, которая находится на заданных
        координатах, и возвращает её.

        Параметры
        ----------
        x : int
            Столбец, где нужно искать шашку.
        y : int
            Строка, где нужно искать шашку.

        Возвращает
        ---------
        Checker или None:
            Объект шашки на указанных координатах или None, если шашки нет.
        """
        for checker in self.game.checkers:
            if checker.x == x and checker.y == y:
                return checker
        return None
