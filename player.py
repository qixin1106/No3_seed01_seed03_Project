import pygame
from config import COLORS, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_Y, WINDOW_WIDTH

class Player:
    def __init__(self):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = (WINDOW_WIDTH - self.width) // 2  # 初始位置在屏幕中间
        self.y = PLAYER_Y
        self.speed = PLAYER_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, keys_pressed, track):
        # 左右移动控制
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.x -= self.speed
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.x += self.speed

        # 边界碰撞检测（赛道边界）
        if self.x <= track.left_border or \
           self.x + self.width >= track.right_border:
            self.x = max(track.left_border, min(self.x, track.right_border - self.width))

        # 更新矩形位置
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        # 绘制玩家车辆（黄色长方形）
        pygame.draw.rect(screen, COLORS['YELLOW'], self.rect)
        # 绘制车辆细节
        pygame.draw.rect(screen, COLORS['BLACK'], self.rect.inflate(-10, -10), 2)
        # 绘制车窗
        window_rect = pygame.Rect(self.x + 15, self.y + 10, self.width - 30, self.height - 60)
        pygame.draw.rect(screen, COLORS['LIGHT_GRAY'], window_rect)
        pygame.draw.rect(screen, COLORS['BLACK'], window_rect, 1)