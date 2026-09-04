#!/usr/bin/env python3
"""
🪱 Worm Game - Інтерактивна гра на основі червячка з CustomTkinter
Модульна архітектура з ООП
"""

from ui.app import GameWindow


def main():
    """Запустити гру"""
    game = GameWindow()
    game.run()


if __name__ == "__main__":
    main()
