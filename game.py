import tkinter as tk

class Game:
    def __init__(self, root, mode="2p"):
        """
        Инициализирует игру.

        Параметры:
        root (tk.Tk): Главное окно приложения.
        """
        self.root = root
        self.mode = mode
        self.limit_moves = 55  # Максимальное количество ходов
        self.current_player = "white"  # Текущий игрок
        self.captured_checkers = {"white": 0, "black": 0}  # Количество побежденных шашек
        self.is_second_move = False
        self.count_moves = 0
        self.checkers = []

        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack(side=tk.TOP)

        self.player_label = tk.Label(self.menu_frame, text=self._get_current_player_text())
        self.player_label.pack(side=tk.LEFT, padx=10)

        self.captured_label = tk.Label(self.menu_frame, text=self._get_captured_label_text())
        self.captured_label.pack(side=tk.LEFT, padx=10)

        self.limit_moves_label = tk.Label(self.menu_frame, text=self._get_limit_moves())
        self.limit_moves_label.pack(side=tk.LEFT, padx=10)

    def add_captured_checker(self, checker):
        """
        Добавляет побежденную шашку и обновляет соответствующий счетчик.

        Параметры:
        checker (Checker): Объект шашки, содержащий информацию о ее цвете.
        """
        print(f"Побежденная шашка: {checker.color}")
        if checker.color in self.captured_checkers:
            self.captured_checkers[checker.color] += 1
            self.captured_label.config(text=self._get_captured_label_text())

    def _get_captured_label_text(self):
        """
        Возвращает текстовое представление количества побежденных шашек.

        Возвращает:
        str: Текст с количеством побежденных белых и черных шашек.
        """
        return f"Побежденные: Белые {self.captured_checkers['white']} - Черные {self.captured_checkers['black']}"

    def switch_player(self):
        """
        Переключает текущего игрока и обновляет отображение в интерфейсе.
        """
        self.count_moves = 0
        self.current_player = "black" if self.current_player == "white" else "white"
        self.player_label.config(text=self._get_current_player_text())
        print(f"Все шашки {self.checkers}")
        self.check_winner()

    def _get_current_player_text(self):
        """
        Возвращает текстовое представление текущего игрока.

        Возвращает:
        str: Текст с указанием текущего игрока.
        """
        return f"Текущий игрок: {self.current_player}"

    def set_limit_moves(self):
        """
        Устанавливает лимит ходов и обновляет отображение в интерфейсе.
        """
        self.limit_moves -= 1
        self.limit_moves_label.config(text=self._get_limit_moves())
        if self.limit_moves <= 0:
            if self.captured_checkers["white"] > self.captured_checkers["black"]:
                self.declare_winner("Черные", "Ходы закончились. Черные победли больше пешек!")
            elif self.captured_checkers["white"] < self.captured_checkers["black"]:
                self.declare_winner("Белые", "Ходы закончились. Белые победли больше пешек!")
            else:
                self.declare_winner("Ничья", "Все ходы закончились")

    def _get_limit_moves(self):
        """
        Возвращает текстовое представление лимита ходов.

        Возвращает:
        str: Текст с указанием количества оставшихся ходов.
        """
        return f"Осталось ходов: {self.limit_moves}"

    def check_winner(self):
        """
        Проверяет, победил ли игрок.
        """
        can_move_black = False
        can_move_white = False

        for checker in self.checkers:
            move1, move2 = checker.find_possible_moves(draw=False)  # Убедитесь, что этот метод работает правильно
            if checker.color == "black" and (move1 or move2):
                can_move_black = True
            if checker.color == "white" and (move1 or move2):
                can_move_white = True

            # Если обе стороны могут двигаться, выходим из метода
            if can_move_black and can_move_white:
                return

        # Проверяем, какие ходы возможны и объявляем победителя или ничью
        if not can_move_black and not can_move_white:
            self.declare_winner("Ничья", "Нет шашек для хода")
        elif not can_move_black:
            self.declare_winner("Белые", "Нет шашек для хода")
        elif not can_move_white:
            self.declare_winner("Черные", "Нет шашек для хода")

    def declare_winner(self, winner, reason):
        """
        Создает окно с объявлением победителя и закрывает приложение при закрытии окна.

        Параметры:
        winner (str): Победитель игры ("white", "black" или "Ничья").
        reason (str): Причина победы или ничьей.
        """
        # Создаем новое окно
        winner_window = tk.Toplevel(self.root)
        winner_window.title("Победитель")

        # Отображаем сообщение о победителе
        winner_label = tk.Label(winner_window, text=f"{winner} победили!" if winner != "Ничья" else "Ничья!", font=("Helvetica", 14))
        winner_label.pack(padx=20, pady=20)

        # Отображаем причину победы/ничьей
        reason_label = tk.Label(winner_window, text=reason, font=("Helvetica", 14))
        reason_label.pack(padx=20, pady=20)

        # Добавляем кнопку для закрытия
        close_button = tk.Button(winner_window, text="Закрыть", command=self._close_game)
        close_button.pack(pady=10)

        # Настройка закрытия окна
        winner_window.protocol("WM_DELETE_WINDOW", self._close_game)

    def _close_game(self):
        """
        Закрывает все окна, включая root.
        """
        self.root.quit()  # Останавливает основной цикл приложения
        from main import show_menu  # Импортируем внутри функции
        self.root.destroy()  # Закрываем окно игры
        show_menu()  # Показываем меню снова