import pygame
import random

class Meteor:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = random.randint(20, 60)
        self.height = self.width  # 保持正方形
        self.x = random.randint(0, screen_width - self.width)
        self.y = -self.height  # 从屏幕顶部外开始
        self.speed = random.randint(1, 5)
        self.color = (139, 69, 19)  # 棕色
        self.active = True

    def update(self):
        # 向下移动
        self.y += self.speed
        # 超出屏幕底部则失效
        if self.y > self.screen_height:
            self.active = False

    def draw(self, screen):
        if self.active:
            # 绘制陨石 - 多边形
            points = []
            num_points = random.randint(5, 10)
            for i in range(num_points):
                angle = i * 360 / num_points
                radius = self.width // 2
                # 添加随机扰动使陨石形状不规则
                random_radius = radius * random.uniform(0.7, 1.3)
                x = self.x + self.width // 2 + random_radius * pygame.math.Vector2.from_polar((1, angle)).x
                y = self.y + self.height // 2 + random_radius * pygame.math.Vector2.from_polar((1, angle)).y
                points.append((x, y))
            pygame.draw.polygon(screen, self.color, points)

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed
