import pygame
from constants import *

class Player:
    def __init__(self):
        self.rect = pygame.Rect(PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.speed = PLAYER_SPEED
        self.color = YELLOW
        
    def update(self, keys, track):
        # 处理横向移动
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            
        # 限制玩家在赛道边界内
        self.rect.x = max(track.left_bound, self.rect.x)
        self.rect.x = min(track.right_bound - self.rect.width, self.rect.x)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # 绘制车辆细节
        pygame.draw.rect(screen, BLACK, self.rect.inflate(-10, -10), 2)
        # 绘制车窗
        pygame.draw.rect(screen, WHITE, (self.rect.x + 10, self.rect.y + 10, self.rect.width - 20, 30))
