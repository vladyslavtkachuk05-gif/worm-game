import customtkinter as ctk
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from ui.styles import Styles
from ui.widgets import GameBoard, GameButton
from models.game_state import GameState
from models.score import ScoreManager
import time


class GameWindow:
    """Головне вікно гри"""
    
    def __init__(self):
        Styles.configure_appearance()
        
        self.root = ctk.CTk()
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT + 100}")
        self.root.title("🪱 Worm Game 🪱")
        self.root.resizable(False, False)
        
        self.game_state = GameState()
        self.score_manager = ScoreManager()
        
        self.running = False
        self.game_started = False
        
        # Таймінги для плавної анімації
        self.last_update_time = 0
        self.update_interval = 1.0 / 6  # 6 оновлень на секунду
        
        self._create_ui()
        self._setup_controls()
        
        self.update_display()
        self.game_loop()
    
    def _create_ui(self):
        """Створити інтерфейс"""
        # Топ панель
        top_frame = ctk.CTkFrame(self.root, fg_color=Styles.DARK_COLOR)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        left_label = ctk.CTkLabel(
            top_frame,
            text="🪱 Worm Game 🪱",
            font=Styles.FONT_LARGE,
            text_color=Styles.ACCENT_COLOR
        )
        left_label.pack(side="left", padx=20)
        
        self.score_label = ctk.CTkLabel(
            top_frame,
            text="Score: 0",
            font=Styles.FONT_MEDIUM,
            text_color=Styles.ACCENT_COLOR
        )
        self.score_label.pack(side="right", padx=20)
        
        # Ігрова дошка
        self.board = GameBoard(self.root)
        self.board.pack(pady=10)
        
        # Нижня панель
        bottom_frame = ctk.CTkFrame(self.root, fg_color=Styles.DARK_COLOR)
        bottom_frame.pack(fill="x", padx=10, pady=10)
        
        self.status_label = ctk.CTkLabel(
            bottom_frame,
            text="Press SPACE to start | Use W A S D to move",
            font=Styles.FONT_NORMAL,
            text_color=Styles.TEXT_COLOR
        )
        self.status_label.pack(pady=10)
        
        # Кнопки
        button_frame = ctk.CTkFrame(bottom_frame, fg_color=Styles.DARK_COLOR)
        button_frame.pack(pady=10)
        
        GameButton(button_frame, text="New Game", command=self.new_game).pack(side="left", padx=5)
        GameButton(button_frame, text="Pause", command=self.toggle_pause, color=Styles.LIGHT_GRAY).pack(side="left", padx=5)
        GameButton(button_frame, text="High Scores", command=self.show_high_scores, color=Styles.LIGHT_GRAY).pack(side="left", padx=5)
        GameButton(button_frame, text="Quit", command=self.quit_game, color=Styles.DANGER_COLOR).pack(side="left", padx=5)
    
    def _setup_controls(self):
        """Налаштувати керування - ТІЛЬКИ WASD"""
        def on_key_press(event):
            key = event.keysym.lower()
            
            if key == "w":
                self.game_state.worm.set_direction(0, -1)
            elif key == "s":
                self.game_state.worm.set_direction(0, 1)
            elif key == "a":
                self.game_state.worm.set_direction(-1, 0)
            elif key == "d":
                self.game_state.worm.set_direction(1, 0)
            elif key == "space":
                self.toggle_game()
            elif key == "r":
                self.new_game()
            elif key == "escape":
                self.quit_game()
        
        self.root.bind("<KeyPress>", on_key_press)
    
    def toggle_game(self):
        """Переключити гру"""
        if not self.game_started:
            self.game_started = True
            self.running = True
            self.status_label.configure(text="Game is running! (SPACE to pause)", text_color=Styles.SUCCESS_COLOR)
        else:
            self.toggle_pause()
    
    def toggle_pause(self):
        """Переключити паузу"""
        self.game_state.toggle_pause()
        if self.game_state.paused:
            self.status_label.configure(text="⏸️ PAUSED (SPACE to continue)", text_color=Styles.LIGHT_GRAY)
            self.running = False
        else:
            self.status_label.configure(text="Game is running! (SPACE to pause)", text_color=Styles.SUCCESS_COLOR)
            self.running = True
    
    def new_game(self):
        """Нова гра"""
        self.game_state.reset()
        self.game_started = False
        self.running = False
        self.score_label.configure(text="Score: 0")
        self.status_label.configure(text="Press SPACE to start | Use W A S D to move", text_color=Styles.TEXT_COLOR)
        self.update_display()
    
    def show_high_scores(self):
        """Показати рекорди"""
        scores = self.score_manager.get_high_scores()
        
        top = ctk.CTkToplevel(self.root)
        top.geometry("400x400")
        top.title("High Scores")
        top.resizable(False, False)
        
        title = ctk.CTkLabel(top, text="🏆 High Scores 🏆", font=Styles.FONT_LARGE, text_color=Styles.ACCENT_COLOR)
        title.pack(pady=20)
        
        if scores:
            for i, (name, score) in enumerate(scores, 1):
                label = ctk.CTkLabel(top, text=f"{i}. {name}: {score}", font=Styles.FONT_NORMAL)
                label.pack(pady=5)
        else:
            label = ctk.CTkLabel(top, text="No scores yet!", font=Styles.FONT_NORMAL, text_color=Styles.LIGHT_GRAY)
            label.pack(pady=20)
        
        GameButton(top, text="Close", command=top.destroy).pack(pady=20)
    
    def update_display(self):
        """Оновити дисплей"""
        state = self.game_state.get_state()
        self.board.draw_game(state["worm_body"], state["food_position"])
        self.score_label.configure(text=f"Score: {state['score']}")
    
    def game_loop(self):
        """Основний цикл гри з плавною анімацією"""
        current_time = time.time()
        
        # Оновлюємо логіку гри з фіксованою частотою
        if self.game_started and self.running and (current_time - self.last_update_time) >= self.update_interval:
            if not self.game_state.update():
                self.running = False
                self.game_started = False
                score = self.game_state.score
                self.status_label.configure(
                    text=f"💀 Game Over! Score: {score} - Press R to restart",
                    text_color=Styles.DANGER_COLOR
                )
                if self.score_manager.is_high_score(score):
                    self.ask_for_name(score)
            
            self.last_update_time = current_time
        
        # Завжди малюємо дисплей (60 FPS)
        self.update_display()
        
        # Планування наступного фрейму (60 FPS)
        self.root.after(16, self.game_loop)  # ~60 FPS (1000ms / 60 = 16.67ms)
    
    def ask_for_name(self, score: int):
        """Запросити ім'я гравця"""
        top = ctk.CTkToplevel(self.root)
        top.geometry("400x200")
        top.title("New High Score!")
        top.resizable(False, False)
        
        title = ctk.CTkLabel(top, text="🌟 New High Score! 🌟", font=Styles.FONT_LARGE, text_color=Styles.SUCCESS_COLOR)
        title.pack(pady=20)
        
        label = ctk.CTkLabel(top, text=f"Score: {score}\nEnter your name:", font=Styles.FONT_NORMAL)
        label.pack(pady=10)
        
        name_entry = ctk.CTkEntry(top, placeholder_text="Player name", font=Styles.FONT_NORMAL, width=250)
        name_entry.pack(pady=10)
        name_entry.focus()
        
        def save_score():
            name = name_entry.get().strip() or "Anonymous"
            self.score_manager.add_score(name, score)
            top.destroy()
        
        GameButton(top, text="Save Score", command=save_score).pack(pady=20)
    
    def quit_game(self):
        """Вихід"""
        self.root.destroy()
    
    def run(self):
        """Запустити"""
        self.root.mainloop()
