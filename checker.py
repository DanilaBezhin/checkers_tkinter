# checker.py
import tkinter as tk
import math

class Checker:
    """
    Класс для представления шашки в игре.

    Атрибуты
    --------
    board : объект
        Объект игрового поля, на котором расположена шашка.
    x : int
        Координата шашки по оси X.
    y : int
        Координата шашки по оси Y.
    size : int
        Размер шашки (диаметр или радиус).
    color : str
        Цвет шашки ('черный' или 'белый').
    is_highlighted : bool
        Указывает, выделена ли шашка для возможного хода.
    available_moves : list
        Список доступных ходов для шашки.
    jump_moves : list
        Список возможных прыжков через другие шашки.

    Методы
    ------
    draw():
        Отрисовывает шашку на доске.
        
    click(event):
        Обрабатывает событие клика по шашке.
    """
    def __init__(self, board, x, y, size, color, game):
        """
        Инициализирует все необходимые атрибуты для объекта Checker.
        """
        self.board = board
        self.game = game
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.is_highlighted = False
        self.available_moves = []
        self.jump_moves = []  
        
        # Отрисовка шашки и привязка события клика
        self.draw()
        self.board.canvas.tag_bind(self.oval, '<Button-1>', self.click)

    def draw(self):
        """
        Отрисовывает или перерисовывает шашку на игровом поле.

        Если шашка уже была нарисована ранее, она удаляется перед отрисовкой новой.
        Также функция рассчитывает координаты для правильного размещения овала (шашки)
        или дуги (для дамок) на доске с небольшим отступом. В зависимости от цвета
        ('black', 'white', 'black-queen', 'white-queen') определяется тип фигуры.
        
        Если шашка выделена, вызывается функция подсветки.
        """
        # Проверяем, если фигура уже существует, удаляем ее
        if hasattr(self, 'oval'):
            self.board.canvas.delete(self.oval)

        # Вычисляем координаты с небольшим отступом
        offset = self.size * 0.1
        x1 = self.x * self.size + offset
        y1 = self.y * self.size + offset
        x2 = x1 + self.size - 2 * offset
        y2 = y1 + self.size - 2 * offset

        # Проверяем, является ли шашка дамкой (черной или белой)
        if self.color == 'black-queen' or self.color == 'white-queen':
            # Определяем цвет для дамки
            fill_color = 'black' if self.color == 'black-queen' else 'white'
            # Рисуем дугу для дамки
            self.oval = self.board.canvas.create_arc(
                x1, y1, x2, y2, start=120, extent=300, fill=fill_color, outline='', width=2
            )
        else:
            # Определяем цвет заливки для обычных шашек
            fill_color = self.color if self.color in ['black', 'white'] else 'gray'
            # Рисуем овал для обычных шашек
            self.oval = self.board.canvas.create_oval(
                x1, y1, x2, y2, fill=fill_color, outline=''
            )

        # Если шашка выделена, вызываем функцию подсветки
        if self.is_highlighted:
            self.highlight()

    def highlight(self):
        """
        Выделяет шашку на доске, изменяя обводку и толщину линии.

        Функция изменяет визуальное представление шашки, добавляя желтую
        обводку и увеличивая толщину линии, чтобы указать, что эта шашка
        сейчас выделена. Также устанавливает флаг `is_highlighted` в `True`,
        чтобы можно было отслеживать текущее состояние выделения.

        Параметры
        ---------
        Нет параметров для входа, так как функция использует текущие атрибуты объекта.
        """
        self.board.canvas.itemconfig(self.oval, outline='yellow', width=3)
        self.is_highlighted = True

    def remove_highlight(self):
        """
        Снимает выделение с шашки и возвращает её к обычному состоянию.

        Функция убирает желтую обводку, уменьшает ширину линии и
        сбрасывает флаг `is_highlighted` в `False`. Также очищает
        любые связанные с этим выделением элементы на доске, такие
        как доступные для хода круги.

        Параметры
        ---------
        Нет параметров для входа, так как функция использует текущие атрибуты объекта.
        """
        self.board.canvas.itemconfig(self.oval, outline='', width=1)
        self.is_highlighted = False
        self.board.clear_available_circles()

    def click(self, event):
        """
        Обрабатывает клик на шашке, выделяя её и определяя возможные ходы.

        При нажатии на шашку выполняется очистка выделений других шашек на доске.
        Если шашка еще не выделена, она выделяется, и вызывается функция для
        нахождения возможных ходов для этой шашки.

        Параметры
        ---------
        event : объект события
            Событие клика мыши, переданное в функцию, используется для
            обработки нажатия.

        Возвращает
        ---------
        Нет.
        """
        if not self.game.is_second_move:
            print(f"{self.game.current_player} = {self.color}")
            if self.color.startswith(self.game.current_player):
                print(self.color, self.game.current_player)
                if not self.board.is_animation:
                    self.board.clear_highlight()
                    
                    print(f"Checker clicked at ({self.x}, {self.y}, {self.color})")
                    if not self.is_highlighted:
                        self.highlight()
                        self.find_possible_moves()

    def find_possible_moves(self, draw=True):
        """
        Определяет возможные ходы и прыжки для шашки.

        Функция вычисляет, какие ходы доступны для текущей шашки в зависимости
        от её цвета и положения на доске. Обычные ходы добавляются в список
        `available_moves`, а возможные прыжки через вражеские шашки добавляются
        в список `jump_moves`. Затем отображаются доступные ходы на доске.

        Параметры
        ---------
        Нет параметров для входа, так как функция использует текущие атрибуты объекта.

        Возвращает
        ---------
        Нет.
        """
        possible_moves = []
        jump_moves = []
        directions = []

        # Определяем направления в зависимости от цвета шашки
        if self.color == "black":
            directions = [(self.x - 1, self.y + 1), (self.x + 1, self.y + 1)]
        elif self.color == "white":
            directions = [(self.x - 1, self.y - 1), (self.x + 1, self.y - 1)]
        elif self.color == "black-queen" or self.color == "white-queen":
            # Дамки могут двигаться в обе стороны
            directions = [
                (self.x - 1, self.y + 1), (self.x + 1, self.y + 1),  # Вниз
                (self.x - 1, self.y - 1), (self.x + 1, self.y - 1)   # Вверх
            ]

        # Проверяем возможные ходы и прыжки
        for move_x, move_y in directions:
            if 0 <= move_x < 8 and 0 <= move_y < 8:
                if (move_x + move_y) % 2 == 1:  # Проверка на черную клетку
                    if not self.is_occupied(move_x, move_y):
                        possible_moves.append((move_x, move_y))
                    elif self.is_enemy_piece(move_x, move_y):  # Проверка на вражескую шашку
                        # Проверяем, можно ли совершить прыжок
                        jump_x = move_x + (move_x - self.x)
                        jump_y = move_y + (move_y - self.y)

                        # Проверка, чтобы дамка не прыгнула через свою шашку
                        if (0 <= jump_x < 8 and 0 <= jump_y < 8 and 
                            not self.is_occupied(jump_x, jump_y) and 
                            self.is_enemy_piece(move_x, move_y)):
                            jump_moves.append((jump_x, jump_y, move_x, move_y))

        self.available_moves = possible_moves
        self.jump_moves = jump_moves

        print("Количество ходов -", self.game.count_moves)
        if self.game.count_moves > 0:
            possible_moves = []
            self.available_moves = []

        if draw:
            self.board.draw_available_circles(possible_moves + [(jm[0], jm[1]) for jm in jump_moves])
        
        # Логирование доступных ходов и прыжков
        print(f"Possible moves for checker at ({self.x}, {self.y}, {self.color}): {possible_moves}")
        print(f"Possible jumps for checker at ({self.x}, {self.y}, {self.color}): {jump_moves}")
        return possible_moves, jump_moves


    def is_enemy_piece(self, x, y):
        """
        Проверяет, является ли шашка на заданной клетке вражеской.

        Параметры
        ----------
        x : int
            Координата по оси X клетки.
        y : int
            Координата по оси Y клетки.

        Возвращает
        -------
        bool
            True, если на клетке находится вражеская шашка, иначе False.
        """
        checker = self.board.get_checker_at(x, y)
        if checker:
            # Если текущая шашка - дамка, то она не может захватывать шашки своего цвета
            if self.color == "black-queen" and checker.color == "black":
                return False
            elif self.color == "white-queen" and checker.color == "white":
                return False
            elif self.color == "black-queen" and checker.color == "white":
                return True
            elif self.color == "white-queen" and checker.color == "black":
                return True
            elif self.color == "white" and (checker.color == "white" or checker.color == "white-queen"):
                return False
            elif self.color == "black" and (checker.color == "black" or checker.color == "black-queen"):
                return False
            elif self.color == "white" and (checker.color == "black" or checker.color == "black-queen"):
                return True
            elif self.color == "black" and (checker.color == "white" or checker.color == "white-queen"):
                return True
        return False

    def is_occupied(self, x, y):
        """
        Проверяет, занята ли заданная клетка.

        Параметры
        ----------
        x : int
            Координата по оси X клетки.
        y : int
            Координата по оси Y клетки.

        Возвращает
        -------
        bool
            True, если клетка занята шашкой, иначе False.
        """
        for checker in self.game.checkers:
            if checker.x == x and checker.y == y:
                return True
        return False

    def animate_move(self, new_x, new_y, steps=20, delay=30, is_jump=False):
        """
        Анимированное перемещение шашки на новую позицию с плавным ускорением и замедлением.

        Параметры
        ----------
        new_x : int
            Новая координата по оси X.
        new_y : int
            Новая координата по оси Y.
        steps : int
            Количество шагов для анимации (чем больше шагов, тем плавнее анимация).
        delay : int
            Задержка между шагами анимации в миллисекундах.
        """
        self.board.clear_available_circles()

        # Начальная позиция
        start_x = self.x
        start_y = self.y

        # Вычисляем смещение
        dx = new_x - start_x
        dy = new_y - start_y

        def update_position(step):
            if step <= steps:
                # Нелинейная интерполяция с использованием синусоиды (эффект ease-in-out)
                t = (1 - math.cos(math.pi * step / steps)) / 2  # плавная кривая

                current_x = start_x + dx * t
                current_y = start_y + dy * t

                # Перерисовываем овал на промежуточных позициях
                self.update_draw(current_x, current_y)

                # Запланировать следующий шаг анимации
                self.board.canvas.after(delay, update_position, step + 1)
            else:
                # По завершению анимации установить точное конечное положение
                self.x = new_x
                self.y = new_y
                self.promote_to_queen()
                print(f"new x - {self.x}, new y - {self.y}")
                self.draw()  # Финальная перерисовка на точной позиции
                self.board.canvas.tag_bind(self.oval, '<Button-1>', self.click)  # Вешаем событие после анимации
                self.board.is_animation = False
                self.board.clear_available_circles()
                self.remove_highlight()  

                if is_jump:
                    a_move, a_jump = self.find_possible_moves()
                    if not a_jump:
                        print(f"доступных ходов в {a_jump} нет, смена игрока, второй хлд - false")
                        self.game.switch_player()  
                        self.remove_highlight()  
                        self.game.is_second_move = False 
                    else:   
                        self.game.is_second_move = True
                        print(f"Есть доступные ходы после первого, второй ход - true")
                        self.highlight()  
                                    

        # Запуск анимации с первого шага
        update_position(0)

    def update_draw(self, current_x, current_y):
        """
        Вспомогательная функция для промежуточного обновления позиции во время анимации.

        Параметры
        ----------
        current_x : float
            Текущая промежуточная координата по оси X.
        current_y : float
            Текущая промежуточная координата по оси Y.
        """
        self.board.is_animation = True
        # Вычисляем координаты овала с небольшим отступом
        offset = self.size * 0.1
        x1 = current_x * self.size + offset
        y1 = current_y * self.size + offset
        x2 = x1 + self.size - 2 * offset
        y2 = y1 + self.size - 2 * offset

        # Удаляем предыдущий овал и рисуем новый на новой позиции
        if hasattr(self, 'oval'):
            self.board.canvas.delete(self.oval)
        
        # Проверяем, является ли шашка дамкой
        if self.color == 'black-queen' or self.color == 'white-queen':
            # Определяем цвет для дамки
            fill_color = 'black' if self.color == 'black-queen' else 'white'
            # Рисуем дугу для дамки
            self.oval = self.board.canvas.create_arc(
                x1, y1, x2, y2, start=120, extent=300, fill=fill_color, outline='', width=2
            )
        else:
            # Рисуем овал для обычных шашек
            self.oval = self.board.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline='')

    def promote_to_queen(self):
        """
        Проверяет, достигла ли шашка конца поля и, если да, меняет ее цвет на дамку.
        """
        if self.color == 'white' and self.y == 0:
            self.color = 'white-queen'
            print("Шашка превращена в дамку: white-queen")
        elif self.color == 'black' and self.y == 7:
            self.color = 'black-queen'
            print("Шашка превращена в дамку: black-queen")
