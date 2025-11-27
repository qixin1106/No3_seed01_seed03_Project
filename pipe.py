import pygame
import random
from constants import HEIGHT, GREEN

class Pipe:
    def __init__(self, x):
        self.width = 32
        self.gap_height = 80
        self.x = x
        self.speed = 2
        self.top_height = random.randint(80, 400 - self.gap_height)
        self.bottom_y = self.top_height + self.gap_height
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, self.bottom_y, self.width, HEIGHT - self.bottom_y - 30)

    def update(self):
        self.x -= self.speed
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)

    def off_screen(self):
        return self.x + self.width < 0

    def passed(self, bird):
        return bird.x > self.x + self.width
