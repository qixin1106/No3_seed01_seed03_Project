import pygame
import random
import math
from settings import *

class Meteor:
    def __init__(self, score=0):
        # 根据分数调整陨石难度
        self.score = score
        self.size = random.randint(METEOR_MIN_SIZE, METEOR_MAX_SIZE)
        self.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.y = -self.size
        
        # 分数越高，陨石速度越快
        speed_multiplier = 1 + (self.score // 1000) * 0.1
        self.speed = random.randint(METEOR_MIN_SPEED, METEOR_MAX_SPEED) * speed_multiplier
        
        self.color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
        # 随机形状（多边形的顶点）
        self.points = self.generate_shape()
        
    def generate_shape(self):
        # 生成随机多边形形状作为陨石
        points = []
        num_points = random.randint(5, 8)
        for i in range(num_points):
            angle = (360 / num_points) * i
            radius = self.size // 2 + random.randint(-5, 5)
            x = self.size // 2 + radius * math.cos(math.radians(angle))
            y = self.size // 2 + radius * math.sin(math.radians(angle))
            points.append((x, y))
        return points
        
    def update(self):
        self.y += self.speed
        self.rect.y = self.y
        
    def draw(self, screen):
        # 绘制陨石多边形
        screen_points = [(self.x + x, self.y + y) for x, y in self.points]
        pygame.draw.polygon(screen, self.color, screen_points)
        pygame.draw.polygon(screen, WHITE, screen_points, 1)
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT
        
    def get_rect(self):
        return self.rect