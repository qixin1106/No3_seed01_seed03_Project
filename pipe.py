import pygame
import random
from config import *

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = PIPE_WIDTH
        self.gap_y = random.randint(80, 400)
        self.top_height = self.gap_y
        self.bottom_y = self.gap_y + PIPE_GAP
        self.bottom_height = WINDOW_HEIGHT - self.bottom_y - 30  # 减去地面高度
        self.passed = False
        
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, self.bottom_y, self.width, self.bottom_height)
    
    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
    
    def draw(self, screen):
        pygame.draw.rect(screen, PIPE_COLOR, self.top_rect)
        pygame.draw.rect(screen, PIPE_COLOR, self.bottom_rect)
    
    def off_screen(self):
        return self.x + self.width < 0
    
    def collides_with(self, bird):
        return self.top_rect.colliderect(bird.rect) or self.bottom_rect.colliderect(bird.rect)
