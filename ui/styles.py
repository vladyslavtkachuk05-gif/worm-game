import customtkinter as ctk
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, TEXT_COLOR, 
    ACCENT_COLOR, GRID_COLOR, DARK_COLOR, LIGHT_GRAY, 
    DANGER_COLOR, SUCCESS_COLOR
)


class Styles:
    """Стилі та кольори"""
    
    FONT_TITLE = ("Arial", 48, "bold")
    FONT_LARGE = ("Arial", 32, "bold")
    FONT_MEDIUM = ("Arial", 20, "bold")
    FONT_NORMAL = ("Arial", 14)
    FONT_SMALL = ("Arial", 12)
    
    BUTTON_WIDTH = 150
    BUTTON_HEIGHT = 50
    
    # Кольори
    BG_COLOR = BG_COLOR
    GRID_COLOR = GRID_COLOR
    TEXT_COLOR = TEXT_COLOR
    ACCENT_COLOR = ACCENT_COLOR
    DARK_COLOR = DARK_COLOR
    LIGHT_GRAY = LIGHT_GRAY
    DANGER_COLOR = DANGER_COLOR
    SUCCESS_COLOR = SUCCESS_COLOR
    
    @staticmethod
    def configure_appearance():
        """Налаштувати CustomTkinter"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
