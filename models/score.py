import json
import os
from typing import List, Tuple
from config import HIGH_SCORES_FILE


class ScoreManager:
    """Управління рекордами"""
    
    def __init__(self):
        self.high_scores: List[Tuple[str, int]] = []
        self.load_scores()
    
    def load_scores(self):
        """Завантажити рекорди"""
        try:
            if os.path.exists(HIGH_SCORES_FILE):
                with open(HIGH_SCORES_FILE, 'r') as f:
                    self.high_scores = json.load(f)
            else:
                self.high_scores = []
        except:
            self.high_scores = []
    
    def save_scores(self):
        """Зберегти рекорди"""
        try:
            os.makedirs(os.path.dirname(HIGH_SCORES_FILE), exist_ok=True)
            with open(HIGH_SCORES_FILE, 'w') as f:
                json.dump(self.high_scores, f)
        except:
            pass
    
    def add_score(self, name: str, score: int):
        """Додати рекорд"""
        self.high_scores.append((name, score))
        self.high_scores.sort(key=lambda x: x[1], reverse=True)
        self.high_scores = self.high_scores[:10]
        self.save_scores()
    
    def is_high_score(self, score: int) -> bool:
        """Чи новий рекорд?"""
        if len(self.high_scores) < 10:
            return True
        return score > self.high_scores[-1][1]
    
    def get_high_scores(self) -> List[Tuple[str, int]]:
        """Отримати рекорди"""
        return self.high_scores.copy()
