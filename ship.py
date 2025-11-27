import pygame

class Ship:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = 50
        self.height = 50
        self.x = (screen_width - self.width) // 2
        self.y = screen_height - self.height - 20
        self.speed = 5
        self.color = (0, 255, 0)  # 绿色
        self.direction = [0, 0]  # [x方向, y方向] -1:左/上, 0:不动, 1:右/下

    def update(self):
        # 根据方向更新位置
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        
        # 边界检测
        self.x = max(0, min(self.screen_width - self.width, self.x))
        self.y = max(0, min(self.screen_height - self.height, self.y))

    def draw(self, screen):
        # 绘制飞船 - 三角形
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(screen, self.color, points)

    def set_direction(self, keys):
        # 根据按键设置方向
        self.direction[0] = 0
        self.direction[1] = 0
        
        if keys[pygame.K_a]:
            self.direction[0] -= 1
        if keys[pygame.K_d]:
            self.direction[0] += 1
        if keys[pygame.K_w]:
            self.direction[1] -= 1
        if keys[pygame.K_s]:
            self.direction[1] += 1

    def get_position(self):
        # 获取飞船中心位置
        return (self.x + self.width // 2, self.y)
