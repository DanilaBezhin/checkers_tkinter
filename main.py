import tkinter as tk
from board import CheckersBoard
from game import Game


def start_game(mode: str, menu_root: tk.Tk) -> None:
    """
    Запускает игру в указанном режиме и закрывает стартовое меню.

    Args:
        mode (str): Режим игры ('Classic', 'Fast', 'AI').
        menu_root (tk.Tk): Окно стартового меню, которое необходимо закрыть.
    """
    menu_root.destroy()

    root = tk.Tk()
    root.title(f"Checkers - {mode} Mode")

    game = Game(root, mode)
    board = CheckersBoard(root, game)

    def end_game() -> None:
        root.destroy()
        show_menu()

    def on_closing() -> None:
        root.destroy()
        show_menu()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


def show_menu() -> None:
    """
    Создаёт стартовое меню с выбором режима игры.
    """
    menu_root = tk.Tk()
    menu_root.title("Select Game Mode")

    label = tk.Label(menu_root, text="Choose Game Mode", font=("Arial", 20))
    label.pack(pady=20)

    classic_button = tk.Button(
        menu_root, text="Classic Mode", font=("Arial", 16),
        command=lambda: start_game("Classic", menu_root)
    )
    classic_button.pack(pady=10)

    fast_button = tk.Button(
        menu_root, text="Fast Mode", font=("Arial", 16),
        command=lambda: start_game("Fast", menu_root)
    )
    fast_button.pack(pady=10)

    ai_button = tk.Button(
        menu_root, text="AI Mode", font=("Arial", 16),
        command=lambda: start_game("AI", menu_root)
    )
    ai_button.pack(pady=10)

    def on_closing() -> None:
        menu_root.destroy()

    close_button = tk.Button(
        menu_root, text="Close", font=("Arial", 16),
        command=on_closing
    )
    close_button.pack(pady=10)

    menu_root.mainloop()


if __name__ == "__main__":
    show_menu()
