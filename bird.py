import pygame
from config import *

class Bird:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.x = WINDOW_WIDTH // 2 - BIRD_SIZE // 2
        self.y = WINDOW_HEIGHT // 3
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, BIRD_SIZE, BIRD_SIZE)
    
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y
    
    def jump(self):
        self.velocity = JUMP_STRENGTH
    
    def draw(self, screen):
        pygame.draw.rect(screen, BIRD_COLOR, self.rect)
