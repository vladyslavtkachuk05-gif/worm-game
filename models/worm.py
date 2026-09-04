from typing import List, Tuple
import random
from config import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, STARTING_LENGTH


class Worm:
    """Класс червячка"""
    
    def __init__(self):
        start_x = 10
        start_y = 10
        
        self.body: List[Tuple[int, int]] = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y),
            (start_x - 3, start_y),
            (start_x - 4, start_y)
        ]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
    
    def move(self) -> Tuple[int, int]:
        """Рухнути червячка"""
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        
        new_x = head_x + self.direction[0]
        new_y = head_y + self.direction[1]
        
        grid_width = WINDOW_WIDTH // GRID_SIZE
        grid_height = WINDOW_HEIGHT // GRID_SIZE
        
        new_x = new_x % grid_width
        new_y = new_y % grid_height
        
        self.body.insert(0, (new_x, new_y))
        return (new_x, new_y)
    
    def remove_tail(self):
        """Видалити хвіст"""
        if len(self.body) > 0:
            self.body.pop()
    
    def check_collision_with_self(self) -> bool:
        """Перевірити зіткнення з собою"""
        head = self.body[0]
        return head in self.body[1:]
    
    def set_direction(self, dx: int, dy: int):
        """Встановити напрямок"""
        if (dx, dy) != (0, 0):
            opposite = (-self.direction[0], -self.direction[1])
            if (dx, dy) != opposite:
                self.next_direction = (dx, dy)
    
    def get_body(self) -> List[Tuple[int, int]]:
        """Отримати все тіло червячка"""
        return self.body.copy()


class Food:
    """Класс їжі"""
    
    def __init__(self):
        self.position = self._generate_position()
    
    def _generate_position(self) -> Tuple[int, int]:
        """Генерувати випадкову позицію"""
        grid_width = WINDOW_WIDTH // GRID_SIZE
        grid_height = WINDOW_HEIGHT // GRID_SIZE
        return (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))
    
    def get_position(self) -> Tuple[int, int]:
        return self.position
    
    def respawn(self, worm_body: List[Tuple[int, int]]):
        """Перепопулювати їжу"""
        while True:
            self.position = self._generate_position()
            if self.position not in worm_body:
                break
