from typing import List, Tuple
from config import STARTING_SPEED, MAX_SPEED
from models.worm import Worm, Food


class GameState:
    """Класс стану гри"""
    
    def __init__(self):
        self.worm = Worm()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.speed = STARTING_SPEED
    
    def update(self) -> bool:
        """Оновити стан гри"""
        if self.game_over or self.paused:
            return not self.game_over
        
        new_head = self.worm.move()
        
        if self.worm.check_collision_with_self():
            self.game_over = True
            return False
        
        if new_head == self.food.get_position():
            self.score += 10
            # Плавне збільшення швидкості
            self.speed = min(self.speed + 0.2, MAX_SPEED)
            self.food.respawn(self.worm.body)
        else:
            self.worm.remove_tail()
        
        return True
    
    def reset(self):
        """Скинути гру"""
        self.worm = Worm()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.speed = STARTING_SPEED
    
    def toggle_pause(self):
        """Переключити паузу"""
        if not self.game_over:
            self.paused = not self.paused
    
    def get_state(self) -> dict:
        """Отримати стан гри"""
        return {
            "worm_body": self.worm.get_body(),
            "food_position": self.food.get_position(),
            "score": self.score,
            "game_over": self.game_over,
            "paused": self.paused,
            "speed": self.speed
        }
