import pygame
from constants import WIDTH, HEIGHT, YELLOW

class Bird:
    def __init__(self):
        self.width = 16
        self.height = 16
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT // 3
        self.velocity = 0
        self.gravity = 0.3
        self.jump_strength = -6
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        self.rect.y = self.y

    def jump(self):
        self.velocity = self.jump_strength

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)
