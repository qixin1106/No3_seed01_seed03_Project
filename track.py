import pygame
import random
from constants import *

class Track:
    def __init__(self):
        self.current_lanes = random.randint(MIN_LANES, MAX_LANES)
        self.target_lanes = self.current_lanes
        self.left_bound = (WINDOW_WIDTH - self.current_lanes * LANE_WIDTH) // 2
        self.right_bound = WINDOW_WIDTH - self.left_bound
        self.target_left = self.left_bound
        self.target_right = self.right_bound
        self.last_change_time = pygame.time.get_ticks()
        
    def update(self):
        current_time = pygame.time.get_ticks()
        
        # 随机切换车道数量（间隔≥3秒）
        if current_time - self.last_change_time >= LANE_CHANGE_INTERVAL:
            self.target_lanes = random.randint(MIN_LANES, MAX_LANES)
            # 确保车道数量变化时赛道宽度平滑过渡
            self.target_left = (WINDOW_WIDTH - self.target_lanes * LANE_WIDTH) // 2
            self.target_right = WINDOW_WIDTH - self.target_left
            self.last_change_time = current_time
            
        # 平滑过渡边界
        if abs(self.left_bound - self.target_left) > LANE_CHANGE_SPEED:
            if self.left_bound < self.target_left:
                self.left_bound += LANE_CHANGE_SPEED
            else:
                self.left_bound -= LANE_CHANGE_SPEED
        else:
            self.left_bound = self.target_left
            
        if abs(self.right_bound - self.target_right) > LANE_CHANGE_SPEED:
            if self.right_bound < self.target_right:
                self.right_bound += LANE_CHANGE_SPEED
            else:
                self.right_bound -= LANE_CHANGE_SPEED
        else:
            self.right_bound = self.target_right
            
    def draw(self, screen):
        # 绘制赛道背景
        pygame.draw.rect(screen, GRAY, (self.left_bound, 0, self.right_bound - self.left_bound, WINDOW_HEIGHT))
        
        # 绘制红色边界
        pygame.draw.rect(screen, RED, (self.left_bound - 10, 0, 10, WINDOW_HEIGHT))
        pygame.draw.rect(screen, RED, (self.right_bound, 0, 10, WINDOW_HEIGHT))
        
        # 绘制白色分隔线
        lane_count = (self.right_bound - self.left_bound) // LANE_WIDTH
        for i in range(1, lane_count):
            x = self.left_bound + i * LANE_WIDTH
            # 绘制虚线
            for y in range(0, WINDOW_HEIGHT, 40):
                pygame.draw.rect(screen, WHITE, (x - 2, y, 4, 20))
