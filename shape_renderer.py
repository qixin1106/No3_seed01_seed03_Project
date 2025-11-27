import pygame
import math
from config import Config

# Ignore pygame static analysis errors
# pyright: reportAttributeAccessIssue=false

class ShapeRenderer:
    def __init__(self, config):
        self.config = config
        self.shape_size = 16  # 16x16 pixel shapes
    
    def draw_shape(self, screen, shape_type, center_x, center_y):
        color = self.config.SHAPE_COLORS[shape_type]
        half_size = self.shape_size // 2
        
        if shape_type == "circle":
            self.draw_circle(screen, color, center_x, center_y, half_size)
        elif shape_type == "square":
            self.draw_square(screen, color, center_x, center_y, half_size)
        elif shape_type == "triangle":
            self.draw_triangle(screen, color, center_x, center_y, half_size)
        elif shape_type == "diamond":
            self.draw_diamond(screen, color, center_x, center_y, half_size)
        elif shape_type == "star":
            self.draw_star(screen, color, center_x, center_y, half_size)
        elif shape_type == "hexagon":
            self.draw_hexagon(screen, color, center_x, center_y, half_size)
        elif shape_type == "heart":
            self.draw_heart(screen, color, center_x, center_y, half_size)
        elif shape_type == "cross":
            self.draw_cross(screen, color, center_x, center_y, half_size)
    
    def draw_circle(self, screen, color, x, y, radius):
        pygame.draw.circle(screen, color, (x, y), radius, 0)
    
    def draw_square(self, screen, color, x, y, size):
        pygame.draw.rect(screen, color, (x - size, y - size, size * 2, size * 2), 0)
    
    def draw_triangle(self, screen, color, x, y, size):
        points = [
            (x, y - size),
            (x - size, y + size),
            (x + size, y + size)
        ]
        pygame.draw.polygon(screen, color, points, 0)
    
    def draw_diamond(self, screen, color, x, y, size):
        points = [
            (x, y - size),
            (x + size, y),
            (x, y + size),
            (x - size, y)
        ]
        pygame.draw.polygon(screen, color, points, 0)
    
    def draw_star(self, screen, color, x, y, size):
        # 5-pointed star
        points = []
        for i in range(5):
            angle = (i * 4 * 3.14159) / 5 - 3.14159 / 2
            radius = size if i % 2 == 0 else size // 2
            px = x + radius * 0.8 * math.cos(angle)
            py = y + radius * 0.8 * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(screen, color, points, 0)
    
    def draw_hexagon(self, screen, color, x, y, size):
        points = []
        for i in range(6):
            angle = (i * 2 * 3.14159) / 6
            px = x + size * 0.8 * math.cos(angle)
            py = y + size * 0.8 * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(screen, color, points, 0)
    
    def draw_heart(self, screen, color, x, y, size):
        # Simple heart shape
        points = [
            (x, y),
            (x - size//2, y - size//2),
            (x - size, y),
            (x - size//2, y + size//2),
            (x, y + size//4),
            (x + size//2, y + size//2),
            (x + size, y),
            (x + size//2, y - size//2)
        ]
        pygame.draw.polygon(screen, color, points, 0)
    
    def draw_cross(self, screen, color, x, y, size):
        # Horizontal line
        pygame.draw.rect(screen, color, (x - size, y - size//3, size * 2, size//1.5), 0)
        # Vertical line
        pygame.draw.rect(screen, color, (x - size//3, y - size, size//1.5, size * 2), 0)
