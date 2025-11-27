import pygame
from settings import *

class Bullet:
    def __init__(self, x, y):
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.x = x - self.width // 2
        self.y = y
        self.speed = BULLET_SPEED
        self.color = BULLET_COLOR
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self):
        self.y -= self.speed
        self.rect.y = self.y
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def is_off_screen(self):
        return self.y + self.height < 0