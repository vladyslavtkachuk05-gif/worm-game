import customtkinter as ctk
from typing import List, Tuple
from config import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE
from ui.styles import Styles


class GameBoard(ctk.CTkCanvas):
    """Ігрова дошка для відображення гри"""
    
    def __init__(self, parent):
        super().__init__(
            parent,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg=Styles.GRID_COLOR,
            highlightthickness=0
        )
    
    def draw_game(self, worm_body: List[Tuple[int, int]], food_position: Tuple[int, int]):
        """Намалювати гру"""
        self.delete("all")
        
        # Фон
        self.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill=Styles.GRID_COLOR, outline=Styles.GRID_COLOR)
        
        # Сітка
        for i in range(0, WINDOW_WIDTH, GRID_SIZE):
            self.create_line(i, 0, i, WINDOW_HEIGHT, fill="#333333", width=1)
        for i in range(0, WINDOW_HEIGHT, GRID_SIZE):
            self.create_line(0, i, WINDOW_WIDTH, i, fill="#333333", width=1)
        
        # Їжа
        self._draw_food(food_position)
        
        # Червячок
        self._draw_worm(worm_body)
    
    def _draw_worm(self, body: List[Tuple[int, int]]):
        """Намалювати червячка"""
        if not body:
            return
        
        for i, (x, y) in enumerate(body):
            x1 = x * GRID_SIZE + 2
            y1 = y * GRID_SIZE + 2
            x2 = (x + 1) * GRID_SIZE - 2
            y2 = (y + 1) * GRID_SIZE - 2
            
            if i == 0:  # Голова
                self.create_rectangle(x1, y1, x2, y2, fill="#ff9500", outline="#ff6b00", width=2)
                self.create_oval(x1 + 4, y1 + 4, x1 + 8, y1 + 8, fill="white")
            else:  # Тіло
                color = "#ffb84d" if i % 2 == 0 else "#ff9500"
                self.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, fill=color, outline="#ff8000")
    
    def _draw_food(self, position: Tuple[int, int]):
        """Намалювати їжу"""
        if not position:
            return
        
        x, y = position
        x1 = x * GRID_SIZE + 4
        y1 = y * GRID_SIZE + 4
        x2 = (x + 1) * GRID_SIZE - 4
        y2 = (y + 1) * GRID_SIZE - 4
        
        self.create_oval(x1, y1, x2, y2, fill="#ff0000", outline="#cc0000", width=2)
        self.create_line((x + 0.5) * GRID_SIZE, y * GRID_SIZE + 2, (x + 0.5) * GRID_SIZE, y * GRID_SIZE - 2, fill="#00aa00", width=2)


class GameButton(ctk.CTkButton):
    """Кастомна кнопка для гри"""
    
    def __init__(self, parent, text: str, command=None, color: str = None, **kwargs):
        fg_color = color if color else Styles.ACCENT_COLOR
        super().__init__(
            parent,
            text=text,
            command=command,
            font=Styles.FONT_MEDIUM,
            fg_color=fg_color,
            width=Styles.BUTTON_WIDTH,
            height=Styles.BUTTON_HEIGHT,
            **kwargs
        )
