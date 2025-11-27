import pygame
from settings import *

class Ship:
    def __init__(self):
        self.width = SHIP_WIDTH
        self.height = SHIP_HEIGHT
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.speed = SHIP_SPEED
        self.color = GREEN
        self.lives = 3
        self.score = 0
        
    def update(self, keys):
        # WASD 控制移动，可以叠加
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
        
        # 边界检测
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        
    def draw(self, screen):
        # 使用多边形绘制飞船
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(screen, self.color, points)
        
        # 绘制飞船边框
        pygame.draw.polygon(screen, WHITE, points, 2)
        
    def reset(self):
        # 重置飞船位置
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.lives = 3
        self.score = 0